#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/twai.h"
#include "driver/gpio.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "ota.h"
#include "discovery.h"

static const char *TAG = "aftline";

// ESP32-S3 pin assignments
#define TRAILER_VOLTAGE_PIN       ADC_CHANNEL_2   // GPIO 2
#define TRAILER_LEFT_TURN_PIN     GPIO_NUM_3
#define TRAILER_RIGHT_TURN_PIN    GPIO_NUM_4
#define TRAILER_BRAKE_PIN         GPIO_NUM_5
#define TRAILER_RUNNING_LIGHT_PIN GPIO_NUM_0

#define CAN_TX_PIN   GPIO_NUM_15
#define CAN_RX_PIN   GPIO_NUM_16

// CAN message identifiers
#define CAN_ID_TRAILER_STATUS  0x10

// CAN transmit period in milliseconds
#define CAN_STATUS_PERIOD_MS   33
#define TX_PROBE_INTERVAL_MS   2000

// ---------------------------------------------------------------------------
// Trailer state (updated by monitor task, read by CAN task)
// ---------------------------------------------------------------------------

typedef struct {
    bool connected;
    uint16_t voltage_mv;
    bool left_turn;
    bool right_turn;
    bool running_lights;
    bool brakes;
} trailer_state_t;

static volatile trailer_state_t s_trailer = {0};

// ---------------------------------------------------------------------------
// ADC handle
// ---------------------------------------------------------------------------

static adc_oneshot_unit_handle_t s_adc_handle = NULL;

// ---------------------------------------------------------------------------
// Trailer monitoring task
// ---------------------------------------------------------------------------

static void trailer_monitor_task(void *arg)
{
    while (1) {
        // Read analog trailer voltage
        int raw = 0;
        adc_oneshot_read(s_adc_handle, TRAILER_VOLTAGE_PIN, &raw);
        // ESP32-S3 ADC is 12-bit (0-4095), 0-3.3V range
        uint16_t mv = (uint16_t)((raw * 3300) / 4095);

        // Read digital inputs (active low with pull-up)
        bool left = gpio_get_level(TRAILER_LEFT_TURN_PIN) == 0;
        bool right = gpio_get_level(TRAILER_RIGHT_TURN_PIN) == 0;
        bool brakes = gpio_get_level(TRAILER_BRAKE_PIN) == 0;
        bool running = gpio_get_level(TRAILER_RUNNING_LIGHT_PIN) == 0;

        // Trailer is connected if voltage exceeds a threshold
        bool connected = (mv > 500);

        s_trailer.voltage_mv = mv;
        s_trailer.left_turn = left;
        s_trailer.right_turn = right;
        s_trailer.brakes = brakes;
        s_trailer.running_lights = running;
        s_trailer.connected = connected;

        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

// ---------------------------------------------------------------------------
// TWAI (CAN) task — runs independently so bus errors never stall monitoring
// ---------------------------------------------------------------------------

static void twai_task(void *arg)
{
    twai_general_config_t g_config = TWAI_GENERAL_CONFIG_DEFAULT(
        CAN_TX_PIN, CAN_RX_PIN, TWAI_MODE_NORMAL);
    twai_timing_config_t t_config = TWAI_TIMING_CONFIG_500KBITS();
    twai_filter_config_t f_config = TWAI_FILTER_CONFIG_ACCEPT_ALL();

    if (twai_driver_install(&g_config, &t_config, &f_config) != ESP_OK) {
        ESP_LOGE(TAG, "Failed to install TWAI driver");
        vTaskDelete(NULL);
        return;
    }
    if (twai_start() != ESP_OK) {
        ESP_LOGE(TAG, "Failed to start TWAI driver");
        vTaskDelete(NULL);
        return;
    }

    uint32_t alerts = TWAI_ALERT_RX_DATA | TWAI_ALERT_ERR_PASS |
                      TWAI_ALERT_BUS_ERROR | TWAI_ALERT_RX_QUEUE_FULL |
                      TWAI_ALERT_BUS_OFF | TWAI_ALERT_BUS_RECOVERED |
                      TWAI_ALERT_ERR_ACTIVE | TWAI_ALERT_TX_FAILED |
                      TWAI_ALERT_TX_SUCCESS;
    twai_reconfigure_alerts(alerts, NULL);
    ESP_LOGI(TAG, "TWAI driver started (NORMAL mode)");

    typedef enum { TX_ACTIVE, TX_PROBING } tx_state_t;
    bool bus_off = false;
    tx_state_t tx_state = TX_ACTIVE;
    int tx_fail_count = 0;
    const int TX_FAIL_THRESHOLD = 3;
    int64_t last_tx_us = 0;
    const int64_t tx_period_us = CAN_STATUS_PERIOD_MS * 1000LL;
    const int64_t tx_probe_period_us = TX_PROBE_INTERVAL_MS * 1000LL;

    while (1) {
        uint32_t triggered;
        twai_read_alerts(&triggered, pdMS_TO_TICKS(CAN_STATUS_PERIOD_MS));

        if (triggered & TWAI_ALERT_BUS_OFF) {
            ESP_LOGE(TAG, "TWAI bus-off, initiating recovery");
            bus_off = true;
            twai_initiate_recovery();
            continue;
        }

        if (triggered & TWAI_ALERT_BUS_RECOVERED) {
            ESP_LOGI(TAG, "TWAI bus recovered, restarting");
            twai_start();
            bus_off = false;
            tx_fail_count = 0;
            tx_state = TX_PROBING;
        }

        if (triggered & TWAI_ALERT_ERR_PASS) {
            ESP_LOGW(TAG, "TWAI error passive (no peers ACKing?)");
        }
        if (triggered & TWAI_ALERT_TX_FAILED) {
            if (tx_state == TX_ACTIVE) {
                tx_fail_count++;
                if (tx_fail_count >= TX_FAIL_THRESHOLD) {
                    tx_state = TX_PROBING;
                    ESP_LOGW(TAG, "TWAI no peers detected, entering slow probe");
                }
            }
        }
        if (triggered & TWAI_ALERT_TX_SUCCESS) {
            if (tx_state == TX_PROBING) {
                tx_state = TX_ACTIVE;
                tx_fail_count = 0;
                ESP_LOGI(TAG, "TWAI probe ACK'd, peer detected, resuming normal TX");
            }
            tx_fail_count = 0;
        }

        // Drain received messages and dispatch
        if (triggered & TWAI_ALERT_RX_DATA) {
            if (tx_state == TX_PROBING) {
                tx_state = TX_ACTIVE;
                tx_fail_count = 0;
                ESP_LOGI(TAG, "TWAI peer detected via RX, resuming normal TX");
            }
            twai_message_t msg;
            while (twai_receive(&msg, 0) == ESP_OK) {
                if (msg.rtr) continue;

                if (msg.identifier == CAN_ID_OTA_TRIGGER) {
                    ota_handle_trigger(msg.data, msg.data_length_code);
                } else if (msg.identifier == CAN_ID_WIFI_CONFIG) {
                    ota_handle_wifi_config(msg.data, msg.data_length_code);
                } else if (msg.identifier == CAN_ID_DISCOVERY_TRIGGER) {
                    discovery_handle_trigger();
                }
            }
        }

        // Periodic transmit (skip if bus is down)
        int64_t now_us = esp_timer_get_time();
        int64_t effective_period = (tx_state == TX_PROBING) ? tx_probe_period_us : tx_period_us;
        if (!bus_off && (now_us - last_tx_us >= effective_period)) {
            last_tx_us = now_us;

            // Pack trailer state into CAN frame:
            //   Byte 0: flags (bit0=connected, bit1=left_turn, bit2=right_turn,
            //                   bit3=running_lights, bit4=brakes)
            //   Byte 1-2: voltage in mV (big-endian)
            trailer_state_t t = s_trailer;
            uint8_t flags = 0;
            if (t.connected)      flags |= 0x01;
            if (t.left_turn)      flags |= 0x02;
            if (t.right_turn)     flags |= 0x04;
            if (t.running_lights) flags |= 0x08;
            if (t.brakes)         flags |= 0x10;

            twai_message_t status_msg = {
                .identifier = CAN_ID_TRAILER_STATUS,
                .data_length_code = 3,
                .data = {
                    flags,
                    (t.voltage_mv >> 8) & 0xFF,
                    t.voltage_mv & 0xFF,
                }
            };

            twai_transmit(&status_msg, 0);
        }
    }
}

// ---------------------------------------------------------------------------
// Main application
// ---------------------------------------------------------------------------

void app_main(void)
{
    ota_init();
    discovery_init();

    // Configure ADC for trailer voltage sensing
    adc_oneshot_unit_init_cfg_t adc_cfg = {
        .unit_id = ADC_UNIT_1,
    };
    adc_oneshot_new_unit(&adc_cfg, &s_adc_handle);

    adc_oneshot_chan_cfg_t chan_cfg = {
        .atten = ADC_ATTEN_DB_12,
        .bitwidth = ADC_BITWIDTH_12,
    };
    adc_oneshot_config_channel(s_adc_handle, TRAILER_VOLTAGE_PIN, &chan_cfg);

    // Configure digital input pins with pull-ups
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << TRAILER_LEFT_TURN_PIN) |
                        (1ULL << TRAILER_RIGHT_TURN_PIN) |
                        (1ULL << TRAILER_BRAKE_PIN) |
                        (1ULL << TRAILER_RUNNING_LIGHT_PIN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);

    ESP_LOGI(TAG, "=== TrailCurrent Aftline ===");
    ESP_LOGI(TAG, "Hostname: %s", ota_get_hostname());

    // Trailer monitoring runs in its own task
    xTaskCreate(trailer_monitor_task, "trailer_mon", 2048, NULL, 10, NULL);

    // CAN runs in its own task so bus errors never block monitoring
    xTaskCreate(twai_task, "twai", 4096, NULL, 5, NULL);
}
