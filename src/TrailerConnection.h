#pragma once
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include <Arduino.h>

typedef struct {
    bool isTrailerConnected;
    float trailerConnectionVoltage;
    bool isLeftTurnOrBrakeOn;
    bool isRightTurnOrBrakeOn;
    bool areTailAndRunningLightsOn;
    float trailerBrakePercentage;
} TrailerConnectionState;

// Handles OTA updates without owning hardware resources
class TrailerConnection {
public:
  static bool begin(gpio_num_t trailer_voltage_pin,
                    gpio_num_t left_turn_or_brake_pin,
                    gpio_num_t right_turn_or_brake_pin,
                    gpio_num_t trailer_brake_pin,
                    gpio_num_t tail_running_light_pin,
                    uint32_t trailerStateChangeTaskStack = 4096,
                    UBaseType_t trailerStateChangeTaskPrio = 16);

  using TrailerStateChangeCallback = void (*)(TrailerConnectionState trailer_connection_state);

  static void onTrailerStateChange(TrailerStateChangeCallback cb);
private:
  static bool _started;
  static float _voltage;
  static bool _isTrailerConnected;
  static gpio_num_t _trailer_voltage_pin;
  static gpio_num_t _left_turn_or_brake_pin;
  static gpio_num_t _right_turn_or_brake_pin;
  static gpio_num_t _trailer_brake_pin;
  static gpio_num_t _tail_running_light_pin;  
  static uint32_t _trailerStateChangeTaskStack;
  static UBaseType_t _trailerStateChangeTaskPrio;
  // Private references to task handles
  static TaskHandle_t _trailerStateChangeTaskHandle;
  // Private Task Queues
  static QueueHandle_t _trailerStateChangeQueue;
  // Private references to callbacks
  static TrailerStateChangeCallback _trailerStateChangeCallback;
  // Private references to the FreeRTOS task hanlders
  static void trailerStateChangeTask(void *);
};
