# TrailCurrent Seven Pin Trailer Monitor

Firmware module that monitors the state of a 7-pin trailer connection including voltage, turn signals, brakes, and running lights, reporting status over a CAN bus interface.

## Overview

- **Microcontroller:** ESP32-C6
- **Function:** 7-pin trailer connector monitoring with CAN bus reporting
- **Key Features:**
  - Monitors trailer voltage, turn signals, brakes, and running lights
  - CAN bus communication at 500 kbps
  - Over-the-air (OTA) firmware updates via WiFi
  - RGB LED status indicator
  - FreeRTOS-based asynchronous monitoring
  - Custom flash partition layout with dual OTA slots

## Hardware Requirements

### Pin Connections

| GPIO | Function |
|------|----------|
| 2 | Trailer voltage sensing (analog) |
| 3 | Left turn/brake line |
| 4 | Right turn/brake line |
| 5 | Electric brake line |
| 0 | Running/tail lights |
| 8 | RGB status LED |
| 15 | CAN TX |
| 14 | CAN RX |

## Firmware

See `src/` directory for PlatformIO-based firmware.

**Setup:**
```bash
# Install PlatformIO (if not already installed)
pip install platformio

# Build firmware
pio run

# Upload to board (serial)
pio run -t upload

# Upload via OTA (after initial flash)
pio run -t upload --upload-port esp32c6-DEVICE_ID
```

### Firmware Dependencies

This firmware depends on the following public libraries:

- **[C6SuperMiniRgbLedLibrary](https://codeberg.org/trailcurrentopensource/C6SuperMiniRgbLedLibrary)** (v0.0.1) - RGB LED status indicator driver
- **[Esp32C6OtaUpdateLibrary](https://codeberg.org/trailcurrentopensource/Esp32C6OtaUpdateLibrary)** (v0.0.1) - Over-the-air firmware update functionality
- **[Esp32C6TwaiTaskBasedLibrary](https://codeberg.org/trailcurrentopensource/Esp32C6TwaiTaskBasedLibrary)** (v0.0.2) - CAN bus communication interface

All dependencies are automatically resolved by PlatformIO during the build process.

**WiFi Credentials (for OTA updates):**
- Copy `src/Secrets.h.example` to `src/Secrets.h` and fill in your WiFi credentials
- Never commit `Secrets.h` to version control (it's in `.gitignore`)

### Monitoring Data

The `TrailerConnection` class tracks:
- Trailer connection voltage (analog reading)
- Left turn/brake signal state
- Right turn/brake signal state
- Tail and running light state
- Electric brake percentage

### CAN Bus Protocol

- **Receive ID `0x00`:** OTA update notifications - triggers firmware update when device ID matches
- Monitoring runs on FreeRTOS core 0 with callback-based state change notifications

## OTA Updates

See `docs/OTA.md` for detailed over-the-air update documentation including the Python upload script.

## Project Structure

```
├── docs/
│   └── OTA.md                    # OTA update documentation
├── src/
│   ├── Main.cpp                  # Main application
│   ├── Globals.h                 # Debug macros and data structures
│   ├── TrailerConnection.cpp     # Trailer monitoring class
│   ├── TrailerConnection.h       # Trailer monitoring header
│   └── Secrets.h.example         # WiFi credentials template
├── platformio.ini                # Build configuration
└── partitions.csv                # ESP32 flash partition layout
```

## License

MIT License - See LICENSE file for details.

## Contributing

Improvements and contributions are welcome! Please submit issues or pull requests.
