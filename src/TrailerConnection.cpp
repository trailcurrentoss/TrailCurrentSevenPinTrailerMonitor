#include "TrailerConnection.h"
// Boolean to track success of the trailer class starting successfully
bool TrailerConnection::_started = false;
float TrailerConnection::_voltage;
bool TrailerConnection::_isTrailerConnected = false;
gpio_num_t TrailerConnection::_trailer_voltage_pin;
gpio_num_t TrailerConnection::_left_turn_or_brake_pin;
gpio_num_t TrailerConnection::_right_turn_or_brake_pin;
gpio_num_t TrailerConnection::_trailer_brake_pin;
gpio_num_t TrailerConnection::_tail_running_light_pin;

// Create task handles
TaskHandle_t TrailerConnection::_trailerStateChangeTaskHandle = nullptr;
// Create the task Queues
QueueHandle_t TrailerConnection::_trailerStateChangeQueue = nullptr;
// Create the callbacks
TrailerConnection::TrailerStateChangeCallback
    TrailerConnection::_trailerStateChangeCallback = nullptr;

bool TrailerConnection::begin(
    gpio_num_t trailer_voltage_pin, gpio_num_t left_turn_or_brake_pin,
    gpio_num_t right_turn_or_brake_pin, gpio_num_t trailer_brake_pin,
    gpio_num_t tail_running_light_pin,
    uint32_t trailerStateChangeTaskStack,
    UBaseType_t trailerStateChangeTaskPrio) {
  // If already started return false
  if (_started)
    return false;

  _left_turn_or_brake_pin = left_turn_or_brake_pin;

  _trailerStateChangeQueue = xQueueCreate(16, sizeof(TrailerConnectionState));
  // If any task queues failed return false
  if (!_trailerStateChangeQueue) {
    return false;
  }

  xTaskCreatePinnedToCore(
      trailerStateChangeTask, "trailerStateChangeTask",
      trailerStateChangeTaskStack, nullptr,
      trailerStateChangeTaskPrio, &_trailerStateChangeTaskHandle, 0);

  pinMode(left_turn_or_brake_pin, INPUT_PULLUP);
  pinMode(right_turn_or_brake_pin, INPUT_PULLUP);
  pinMode(trailer_brake_pin, INPUT_PULLUP);
  pinMode(tail_running_light_pin, INPUT_PULLUP);
  // Set the _started in case begin is called again.
  _started = true;
  return true;
}
// Callback mappings
void TrailerConnection::onTrailerStateChange(
    TrailerStateChangeCallback cb) {
  _trailerStateChangeCallback = cb;
}

void TrailerConnection::trailerStateChangeTask(void *) {
  while (true) {
    TrailerConnectionState returnValue;
    int rawValue = analogRead(_trailer_voltage_pin); // Reads 0-4095
    float _voltage = rawValue * (3.3 / 4095.0);      // Convert to 0-3.3V
    returnValue.trailerConnectionVoltage = _voltage;
    _trailerStateChangeCallback(returnValue);
  }
}
