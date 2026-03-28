# TrailCurrent Aftline

Firmware module that monitors the state of a 7-pin trailer connection including voltage, turn signals, brakes, and running lights, reporting status over a CAN bus interface. Part of the [TrailCurrent](https://trailcurrent.com) open-source vehicle platform.

## Overview

- **Hardware:** [Waveshare ESP32-S3-RS485-CAN](https://www.waveshare.com/esp32-s3-rs485-can.htm) — industrial-grade board with isolated CAN and RS485 interfaces, 7-36V DC input, ESP32-S3-WROOM-1 (16MB flash, 8MB PSRAM)
- **Framework:** ESP-IDF (Espressif IoT Development Framework)
- **Function:** Trailer connector monitoring with CAN bus reporting
- **Key Features:**
  - Monitors trailer voltage, turn signals, brakes, and running lights
  - CAN bus communication at 500 kbps
  - Over-the-air (OTA) firmware updates via HTTP
  - mDNS device discovery for Headwaters integration
  - WiFi credential provisioning via CAN bus
  - FreeRTOS-based asynchronous monitoring
  - Custom flash partition layout with dual OTA slots

## Hardware

### Pin Connections

| GPIO | Function |
|------|----------|
| 2 | Trailer voltage sensing (ADC) |
| 3 | Left turn/brake line (digital input) |
| 4 | Right turn/brake line (digital input) |
| 5 | Electric brake line (digital input) |
| 0 | Running/tail lights (digital input) |
| 15 | CAN TX (onboard isolated transceiver) |
| 16 | CAN RX (onboard isolated transceiver) |

### Onboard Interfaces (provided by board)

- **CAN:** Isolated, 120-ohm termination resistor (jumper-selectable)
- **RS485:** Isolated, GPIO17 TX / GPIO18 RX / GPIO21 EN
- **Power:** 7-36V DC via screw terminal or 5V via USB-C
- **USB:** Type-C for programming and debugging

## Firmware

### Prerequisites

Install ESP-IDF v5.x following the [official guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/).

### Build and Flash

```bash
# Set target to ESP32-S3
idf.py set-target esp32s3

# Build firmware
idf.py build

# Flash to board (serial)
idf.py -p /dev/ttyACM0 flash

# Monitor serial output
idf.py -p /dev/ttyACM0 monitor
```

### WiFi Credential Provisioning

WiFi credentials are provisioned over the CAN bus (ID `0x01`) using a chunked protocol. No hardcoded credentials are needed. The protocol works as follows:

1. **Start** `[0x01, ssid_len, password_len, ssid_chunks, password_chunks]`
2. **SSID chunks** `[0x02, chunk_index, up to 6 bytes]` (repeat for each chunk)
3. **Password chunks** `[0x03, chunk_index, up to 6 bytes]` (repeat for each chunk)
4. **End** `[0x04, xor_checksum]`

Credentials are stored in NVS and persist across reboots.

### CAN Bus Protocol

**Speed:** 500 kbps

#### Receive Messages

| ID | Function |
|----|----------|
| `0x00` | OTA trigger — 3 bytes matching last 3 MAC bytes of target device |
| `0x01` | WiFi credential provisioning (chunked protocol) |
| `0x02` | Discovery trigger (broadcast, no payload) |

#### Transmit Messages

| ID | Period | Function |
|----|--------|----------|
| `0x10` | 33 ms | Trailer status (3 bytes) |

**Trailer Status Frame (0x10):**
- Byte 0: Flags — `bit0`=connected, `bit1`=left turn, `bit2`=right turn, `bit3`=running lights, `bit4`=brakes
- Byte 1-2: Trailer voltage in mV (big-endian)

### OTA Firmware Updates

OTA updates are triggered via CAN message ID `0x00` containing the last 3 bytes of the target device's MAC address. The device then:

1. Connects to WiFi using stored credentials
2. Starts an HTTP server with mDNS advertising (`{hostname}.local`)
3. Accepts firmware upload at `POST /ota`
4. Waits up to 3 minutes for an upload before returning to normal operation

```bash
# Upload firmware to a specific device
curl -X POST http://esp32-XXYYZZ.local/ota --data-binary @build/aftline.bin
```

### Device Discovery

Discovery is triggered via CAN broadcast (ID `0x02`). The device:

1. Connects to WiFi
2. Advertises `_trailcurrent._tcp` mDNS service with TXT records:
   - `type=aftline`
   - `canid=0x10`
   - `fw={version}`
3. Waits up to 3 minutes for Headwaters to confirm at `GET /discovery/confirm`

## Project Structure

```
├── main/
│   ├── main.c               # Application entry point, trailer monitoring, CAN task
│   ├── ota.c                 # OTA updates, WiFi management, credential provisioning
│   ├── ota.h                 # OTA public API
│   ├── discovery.c           # mDNS device discovery
│   ├── discovery.h           # Discovery public API
│   ├── CMakeLists.txt        # Component build configuration
│   └── idf_component.yml     # Managed dependencies
├── CMakeLists.txt            # Top-level ESP-IDF project configuration
├── partitions.csv            # ESP32-S3 flash partition layout
├── sdkconfig.defaults        # Default build configuration
└── README.md                 # This file
```

## License

MIT License - See LICENSE file for details.

## Contributing

Improvements and contributions are welcome! Please submit issues or pull requests.
