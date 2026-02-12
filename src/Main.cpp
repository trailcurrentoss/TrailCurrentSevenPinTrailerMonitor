#include "Globals.h"
#include <OtaUpdate.h>
#include <RgbLed.h>
#include "TrailerConnection.h"
#include <Arduino.h>
#include <driver/gpio.h>
#include "Secrets.h"
#include <TwaiTaskBased.h>
// Define the pins we'll be using
#define TRAILER_VOLTAGE_PIN 2
#define TRAILER_LEFT_TURN_OR_BRAKE 3
#define TRAILER_RIGHT_TURN_OR_BRAKE 4
#define TRAILER_BRAKE_PIN 5
#define TRAILER_RUNNING_LIGHT_PIN 0

RgbLed statusLed(8);
OtaUpdate otaUpdate(statusLed, 60000, ssid, password);

void onCanRx(const twai_message_t &msg) {
  debugf("RX ID: 0x%X DLC: %d\n", msg.identifier, msg.data_length_code);
  // We received a CAN bus message that may mean an update is available.
  if (msg.identifier == 0) {
    // Create a char to hold the name of who the update is for.
    char updateForHostName[14];
    // Get the current host name of this device
    String currentHostName = otaUpdate.getHostName();
    // Fomrat the string of the upate so it matches the pattern used by
    // espressif
    sprintf(updateForHostName, "esp32c6-%X%X%X", msg.data[0], msg.data[1],
            msg.data[2]);
    // An update is ready for this device if the two match.
    if (currentHostName.equals(updateForHostName)) {
      debugln("Need to wait for OTA");
      // Pause and see if an OTA is needed
      otaUpdate.waitForOta();
    }
  }
}

void onCanTx(bool ok) { debugln(ok ? "TX OK" : "TX FAIL"); }

void onTrailerStateChange(TrailerConnectionState trailer_connection_state) {
  debugln("New state:");
  debugf("isTrailerConnected: %d\n", trailer_connection_state.isTrailerConnected);
}

void setup() {
  // Always start serial even if only to output that debugging is disabled.
  Serial.begin(115200);
// These should be the only two Serial.print statements. All others will use
// debug, debugln, and debugf so they are removed for production.
#if DEBUG == 0
  Serial.println(
      "Debugging is disabled no more output will be written here...");
#else
  Serial.println("Debugging started");
#endif
  // Initialize the onboard LED first so we can use it to communicate status.
  statusLed.begin();
  statusLed.setBrightnessPercent(1);
  // Now set the callbacks and initialize the CAN helper.
  TwaiTaskBased::onReceive(onCanRx);
  TwaiTaskBased::onTransmit(onCanTx);
  TwaiTaskBased::begin(GPIO_NUM_15, GPIO_NUM_14);
  // Register all the callbacks and start the TrailerConnection
  TrailerConnection::onTrailerStateChange(onTrailerStateChange);
  TrailerConnection::begin((gpio_num_t)TRAILER_VOLTAGE_PIN, (gpio_num_t)TRAILER_LEFT_TURN_OR_BRAKE, (gpio_num_t)TRAILER_RIGHT_TURN_OR_BRAKE,(gpio_num_t)TRAILER_BRAKE_PIN, (gpio_num_t)TRAILER_RUNNING_LIGHT_PIN);
  statusLed.green();
  debugln("Setup done");
}

void loop() {
  twai_message_t msg = {};
  msg.identifier = 0x123;
  msg.data_length_code = 2;
  msg.data[0] = 0xAB;
  msg.data[1] = 0xCD; 

  // TwaiTaskBased::send(msg);
}
