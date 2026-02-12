#pragma once
#ifndef GLOBALS_H
#define GLOBALS_H
#define DEBUG 1 // This sets whether or not the Serial.println and Serial.print will even be compiled
// Conditional definition for debugging if DEBUG is 1 then it will print to serial port.
// If DEBUG = 0 then the lines will be removed by the compiler.
#if DEBUG == 1
#define debug(...) Serial.print(##__VA_ARGS__)
#define debugln(x) Serial.println(x)
#define debugw(...) Serial.write(##__VA_ARGS__)
#define debugf(x, ...) Serial.printf(x, ##__VA_ARGS__)
#else
#define debug(...)
#define debugln(...)
#define debugw(...)
#define debugf(x, ...)
#endif

struct trailer_connector_data_t {
  bool tail_or_running_status;
  bool left_turn_or_brake_status;
  bool right_turn_or_brake_status; 
  bool reverse_status; 
  unsigned int electric_brake_status;
  unsigned int twelve_volt_reading;
};

#endif // GLOBALS_H