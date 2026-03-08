#!/usr/bin/env python3
"""Generate KiCAD 9.0 schematic for TrailCurrent Aftline.

Usage: python3 generate_schematic.py
Outputs: TrailCurrentAftline/TrailCurrentAftline.kicad_sch

Circuit Design:
- ESP32-C6 SuperMini MCU
- Mini560 Buck Converter (12V → 5V)
- SN65HVD230DR CAN Transceiver
- 4x TLP290 Optocouplers (L Turn, R Turn, Running Lights, Backup Lights)
- 2x Voltage Dividers (Aux 12V sensing, Trailer Brakes analog)
- S8B-XH-SM4-TB 8-pin trailer input connector
- S4B-XH-SM4-TB 4-pin CAN+power connector
"""

import uuid
import os

ROOT_UUID = "86f98bd6-ce0d-455d-9e10-e9c66bf3b7ae"
PROJECT_NAME = "TrailCurrentAftline"

def uid():
    return str(uuid.uuid4())

# ============================================================================
# EMBEDDED SYMBOL DEFINITIONS (lib_symbols section)
# ============================================================================

LIB_SYMBOLS = """
	(lib_symbols
		(symbol "Device:C"
			(pin_numbers (hide yes))
			(pin_names (offset 0.254))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "" (at 0.9652 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Unpolarized capacitor" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_keywords" "cap capacitor" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_fp_filters" "C_*" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "C_0_1"
				(polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
			)
			(symbol "C_1_1"
				(pin passive line (at 0 3.81 270) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 2.794) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "Device:R"
			(pin_numbers (hide yes))
			(pin_names (offset 0))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
			(property "Value" "R" (at 0 0 90) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at -1.778 0 90) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Resistor" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_keywords" "R res resistor" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_fp_filters" "R_*" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "R_0_1"
				(rectangle (start -1.016 -2.54) (end 1.016 2.54) (stroke (width 0.254) (type default)) (fill (type none)))
			)
			(symbol "R_1_1"
				(pin passive line (at 0 3.81 270) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -3.81 90) (length 1.27) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "Isolator:TLP290"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U" (at -5.08 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Value" "TLP290" (at 0 5.08 0) (effects (font (size 1.27 1.27)) (justify left)))
			(property "Footprint" "Package_SO:SOP-4_4.4x2.6mm_P1.27mm" (at -21.59 -5.08 0) (effects (font (size 1.27 1.27) (italic yes)) (justify left) (hide yes)))
			(property "Datasheet" "https://toshiba.semicon-storage.com/info/docget.jsp?did=12882&prodName=TLP290" (at 0.635 0 0) (effects (font (size 1.27 1.27)) (justify left) (hide yes)))
			(property "Description" "AC/DC Phototransistor Optocoupler, Vce 80V, CTR 50-600%, SOP4" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_keywords" "NPN AC DC Phototransistor Optocoupler" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_fp_filters" "SOP*4*4.4x2.6mm*P1.27mm*" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "TLP290_0_1"
				(rectangle (start -5.08 3.81) (end 5.08 -3.81) (stroke (width 0.254) (type default)) (fill (type background)))
				(polyline (pts (xy -5.08 2.54) (xy -1.27 2.54) (xy -1.27 -0.635)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy -3.81 0.635) (xy -2.54 0.635)) (stroke (width 0.254) (type default)) (fill (type none)))
				(circle (center -3.175 2.54) (radius 0.127) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy -3.175 0.635) (xy -3.81 -0.635) (xy -2.54 -0.635) (xy -3.175 0.635)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy -3.175 -0.635) (xy -3.175 2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy -3.175 -0.635) (xy -3.175 -2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(circle (center -3.175 -2.54) (radius 0.127) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy -1.905 -0.635) (xy -0.635 -0.635)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy -1.27 -0.635) (xy -1.27 -2.54) (xy -5.08 -2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy -1.27 -0.635) (xy -1.905 0.635) (xy -0.635 0.635) (xy -1.27 -0.635)) (stroke (width 0.254) (type default)) (fill (type none)))
				(polyline (pts (xy 0.127 0.508) (xy 1.397 0.508) (xy 1.016 0.381) (xy 1.016 0.635) (xy 1.397 0.508)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0.127 -0.508) (xy 1.397 -0.508) (xy 1.016 -0.635) (xy 1.016 -0.381) (xy 1.397 -0.508)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 2.54 1.905) (xy 2.54 -1.905)) (stroke (width 0.508) (type default)) (fill (type none)))
				(polyline (pts (xy 2.54 0.635) (xy 4.445 2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 3.048 -1.651) (xy 3.556 -1.143) (xy 4.064 -2.159) (xy 3.048 -1.651)) (stroke (width 0) (type default)) (fill (type outline)))
				(polyline (pts (xy 4.445 2.54) (xy 5.08 2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 4.445 -2.54) (xy 2.54 -0.635)) (stroke (width 0) (type default)) (fill (type outline)))
				(polyline (pts (xy 4.445 -2.54) (xy 5.08 -2.54)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "TLP290_1_1"
				(pin passive line (at -7.62 2.54 0) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at -7.62 -2.54 0) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 7.62 2.54 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 7.62 -2.54 180) (length 2.54) (name "~" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "Mechanical:MountingHole"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom no)
			(on_board yes)
			(property "Reference" "H" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
			(property "Value" "MountingHole" (at 0 3.175 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Mounting Hole without connection" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_keywords" "mounting hole" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "ki_fp_filters" "MountingHole*" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "MountingHole_0_1"
				(circle (center 0 0) (radius 1.27) (stroke (width 1.27) (type default)) (fill (type none)))
			)
			(embedded_fonts no)
		)
		(symbol "TrailCurrentSymbolLibrary:ESP32-C6-SuperMini"
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U" (at 12.7 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "ESP32-C6-SuperMini" (at 12.7 0 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "TrailCurrentFootprints:ESP32-C6-SuperMini_SMD" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "https://www.espboards.dev/esp32/esp32-c6-super-mini/" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "ESP32-C6 Super Mini Development Board, WiFi 6, BLE 5, Zigbee, Thread" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "ESP32-C6-SuperMini_0_1"
				(rectangle (start 5.08 1.27) (end 20.32 -24.13) (stroke (width 0.254) (type default)) (fill (type background)))
				(pin bidirectional line (at 0 0 0) (length 5.08) (name "TX" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -2.54 0) (length 5.08) (name "RX" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -5.08 0) (length 5.08) (name "GPIO0" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -7.62 0) (length 5.08) (name "GPIO1" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -10.16 0) (length 5.08) (name "GPIO2" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -12.7 0) (length 5.08) (name "GPIO3" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -15.24 0) (length 5.08) (name "GPIO4" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -17.78 0) (length 5.08) (name "GPIO5" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -20.32 0) (length 5.08) (name "GPIO6" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 0 -22.86 0) (length 5.08) (name "GPIO7" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 25.4 0 180) (length 5.08) (name "5V" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 25.4 -2.54 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 25.4 -5.08 180) (length 5.08) (name "3V3" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 25.4 -7.62 180) (length 5.08) (name "GPIO20" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 25.4 -10.16 180) (length 5.08) (name "GPIO19" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 25.4 -12.7 180) (length 5.08) (name "GPIO18" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 25.4 -15.24 180) (length 5.08) (name "GPIO15" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 25.4 -17.78 180) (length 5.08) (name "GPIO14" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 25.4 -20.32 180) (length 5.08) (name "GPIO9" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
				(pin bidirectional line (at 25.4 -22.86 180) (length 5.08) (name "GPIO8" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "TrailCurrentSymbolLibrary:Mini560"
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "U" (at 12.7 2.54 0) (effects (font (size 1.27 1.27))))
			(property "Value" "Mini560" (at 12.7 0 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "TrailCurrentFootprints:Mini560" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Mini560 DC-DC Buck Converter Module, 5A, 7-20V to 3.3/5/9/12V" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "Mini560_0_1"
				(rectangle (start 5.08 1.27) (end 20.32 -20.32) (stroke (width 0.254) (type default)) (fill (type background)))
				(pin power_in line (at 0 0 0) (length 5.08) (name "VIN+" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -2.54 0) (length 5.08) (name "VIN+" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin power_in line (at 0 -5.08 0) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -7.62 0) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin input line (at 12.7 -25.4 90) (length 5.08) (name "EN" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 25.4 -7.62 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 25.4 -5.08 180) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin power_out line (at 25.4 -2.54 180) (length 5.08) (name "VOUT+" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 25.4 0 180) (length 5.08) (name "VOUT+" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "TrailCurrentSymbolLibrary:S4B-XH-SM4-TB"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "J" (at -3.81 5.715 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
			(property "Value" "S4B-XH-SM4-TB" (at -3.81 -10.16 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
			(property "Footprint" "TrailCurrentFootprints:JST_S4B-XH-SM4-TB" (at 0 0 0) (effects (font (size 1.27 1.27)) (justify bottom) (hide yes)))
			(property "Datasheet" "https://www.jst-mfg.com/product/pdf/eng/eXH.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "JST XH 4-pin SMD Connector, 2.50mm Pitch, Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "S4B-XH-SM4-TB_0_0"
				(rectangle (start -3.81 -7.62) (end 5.08 5.08) (stroke (width 0.254) (type default)) (fill (type background)))
				(rectangle (start -3.175 2.2225) (end -1.5875 2.8575) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -0.3175) (end -1.5875 0.3175) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -2.8575) (end -1.5875 -2.2225) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -5.3975) (end -1.5875 -4.7625) (stroke (width 0.1) (type default)) (fill (type outline)))
				(pin passive line (at -7.62 2.54 0) (length 5.08) (name "1" (effects (font (size 1.016 1.016)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 0 0) (length 5.08) (name "2" (effects (font (size 1.016 1.016)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 -2.54 0) (length 5.08) (name "3" (effects (font (size 1.016 1.016)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 -5.08 0) (length 5.08) (name "4" (effects (font (size 1.016 1.016)))) (number "4" (effects (font (size 1.016 1.016)))))
			)
			(embedded_fonts no)
		)
		(symbol "TrailCurrentSymbolLibrary:S8B-XH-SM4-TB"
			(pin_names (offset 1.016))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "J" (at -3.81 10.795 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
			(property "Value" "S8B-XH-SM4-TB" (at -3.81 -20.32 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
			(property "Footprint" "TrailCurrentFootprints:JST_S8B-XH-SM4-TB" (at 0 0 0) (effects (font (size 1.27 1.27)) (justify bottom) (hide yes)))
			(property "Datasheet" "https://www.jst-mfg.com/product/pdf/eng/eXH.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "JST XH 8-pin SMD Connector, 2.50mm Pitch, Horizontal" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "S8B-XH-SM4-TB_0_0"
				(rectangle (start -3.81 -17.78) (end 5.08 10.16) (stroke (width 0.254) (type default)) (fill (type background)))
				(rectangle (start -3.175 7.3025) (end -1.5875 7.9375) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 4.7625) (end -1.5875 5.3975) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 2.2225) (end -1.5875 2.8575) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -0.3175) (end -1.5875 0.3175) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -2.8575) (end -1.5875 -2.2225) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -5.3975) (end -1.5875 -4.7625) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -7.9375) (end -1.5875 -7.3025) (stroke (width 0.1) (type default)) (fill (type outline)))
				(rectangle (start -3.175 -10.4775) (end -1.5875 -9.8425) (stroke (width 0.1) (type default)) (fill (type outline)))
				(pin passive line (at -7.62 7.62 0) (length 5.08) (name "1" (effects (font (size 1.016 1.016)))) (number "1" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 5.08 0) (length 5.08) (name "2" (effects (font (size 1.016 1.016)))) (number "2" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 2.54 0) (length 5.08) (name "3" (effects (font (size 1.016 1.016)))) (number "3" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 0 0) (length 5.08) (name "4" (effects (font (size 1.016 1.016)))) (number "4" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 -2.54 0) (length 5.08) (name "5" (effects (font (size 1.016 1.016)))) (number "5" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 -5.08 0) (length 5.08) (name "6" (effects (font (size 1.016 1.016)))) (number "6" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 -7.62 0) (length 5.08) (name "7" (effects (font (size 1.016 1.016)))) (number "7" (effects (font (size 1.016 1.016)))))
				(pin passive line (at -7.62 -10.16 0) (length 5.08) (name "8" (effects (font (size 1.016 1.016)))) (number "8" (effects (font (size 1.016 1.016)))))
			)
			(embedded_fonts no)
		)
		(symbol "TrailCurrentSymbolLibrary:SN65HVD230DR"
			(in_bom yes)
			(on_board yes)
			(property "Reference" "IC" (at 24.13 7.62 0) (effects (font (size 1.27 1.27)) (justify left top)))
			(property "Value" "SN65HVD230DR" (at 24.13 5.08 0) (effects (font (size 1.27 1.27)) (justify left top)))
			(property "Footprint" "TrailCurrentFootprints:SN65HVD230DR" (at 24.13 -94.92 0) (effects (font (size 1.27 1.27)) (justify left top) (hide yes)))
			(property "Datasheet" "http://www.ti.com/lit/gpn/sn65hvd230" (at 24.13 -194.92 0) (effects (font (size 1.27 1.27)) (justify left top) (hide yes)))
			(property "ki_description" "3.3 V CAN Transceiver with Standby Mode" (at 24.13 -294.92 0) (effects (font (size 1.27 1.27)) (justify left top) (hide yes)))
			(symbol "SN65HVD230DR_0_1"
				(rectangle (start 5.08 2.54) (end 22.86 -10.16) (stroke (width 0.254) (type default)) (fill (type background)))
				(pin passive line (at 0 0 0) (length 5.08) (name "D" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -2.54 0) (length 5.08) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -5.08 0) (length 5.08) (name "VCC" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 0 -7.62 0) (length 5.08) (name "R" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 27.94 0 180) (length 5.08) (name "VREF" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 27.94 -2.54 180) (length 5.08) (name "CANL" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 27.94 -5.08 180) (length 5.08) (name "CANH" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
				(pin passive line (at 27.94 -7.62 180) (length 5.08) (name "RS" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
			)
		)
		(symbol "power:+12V"
			(power)
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+12V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Power symbol creates a global label with name \\\"+12V\\\"" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+12V_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+12V_1_1"
				(pin power_in line (at 0 0 90) (length 0) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "power:+3.3V"
			(power)
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+3.3V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Power symbol creates a global label with name \\\"+3.3V\\\"" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+3.3V_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+3.3V_1_1"
				(pin power_in line (at 0 0 90) (length 0) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "power:+5V"
			(power)
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "+5V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Power symbol creates a global label with name \\\"+5V\\\"" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "+5V_0_1"
				(polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
				(polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "+5V_1_1"
				(pin power_in line (at 0 0 90) (length 0) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
		(symbol "power:GND"
			(power)
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
			(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(property "Description" "Power symbol creates a global label with name \\\"GND\\\" , ground" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
			(symbol "GND_0_1"
				(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
			)
			(symbol "GND_1_1"
				(pin power_in line (at 0 0 270) (length 0) (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
			)
			(embedded_fonts no)
		)
	)
"""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

pwr_counter = [0]

def make_wire(x1, y1, x2, y2):
    return f'\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))\n'

def make_global_label(name, x, y, angle=0, shape="bidirectional"):
    return f"""\t(global_label "{name}"
\t\t(shape {shape})
\t\t(at {x} {y} {angle})
\t\t(effects (font (size 1.27 1.27)))
\t\t(uuid "{uid()}")
\t\t(property "Intersheets" ""
\t\t\t(at {x} {y} {angle})
\t\t\t(effects (font (size 1.016 1.016)) (hide yes))
\t\t)
\t)
"""

def make_no_connect(x, y):
    return f'\t(no_connect (at {x} {y}) (uuid "{uid()}"))\n'

def make_junction(x, y):
    return f'\t(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))\n'

def make_text(text, x, y, size=2.54):
    return f"""\t(text "{text}"
\t\t(exclude_from_sim no)
\t\t(at {x} {y} 0)
\t\t(effects (font (size {size} {size})) (justify left))
\t\t(uuid "{uid()}")
\t)
"""

def make_power_symbol(lib_name, value, ref_num, x, y, angle=0):
    """Place a power symbol (GND, +3.3V, +5V, +12V)."""
    pwr_counter[0] += 1
    ref = f"#PWR0{pwr_counter[0]:02d}"
    return f"""\t(symbol
\t\t(lib_id "power:{value}")
\t\t(at {x} {y} {angle})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x} {y + (-3.81 if value == "GND" else 3.81)} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x} {y + (-2.54 if value == "GND" else 2.54)} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" ""
\t\t\t(at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(instances
\t\t\t(project "{PROJECT_NAME}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
"""

def make_component(lib_id, ref, value, footprint, x, y, angle, pin_count,
                   ref_offset_x=0, ref_offset_y=-3, val_offset_x=0, val_offset_y=-5):
    """Place a component symbol on the schematic."""
    pins = "\n".join(f'\t\t(pin "{i}" (uuid "{uid()}"))' for i in range(1, pin_count + 1))
    return f"""\t(symbol
\t\t(lib_id "{lib_id}")
\t\t(at {x} {y} {angle})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x + ref_offset_x} {y + ref_offset_y} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "{value}"
\t\t\t(at {x + val_offset_x} {y + val_offset_y} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "{footprint}"
\t\t\t(at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
{pins}
\t\t(instances
\t\t\t(project "{PROJECT_NAME}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
"""

def make_mounting_hole(ref, x, y):
    """Place a mounting hole."""
    return f"""\t(symbol
\t\t(lib_id "Mechanical:MountingHole")
\t\t(at {x} {y} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom no)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {x} {y - 5.08} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "MountingHole"
\t\t\t(at {x} {y - 3.175} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "MountingHole:MountingHole_2.5mm"
\t\t\t(at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (hide yes))
\t\t)
\t\t(instances
\t\t\t(project "{PROJECT_NAME}"
\t\t\t\t(path "/{ROOT_UUID}"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
"""


# ============================================================================
# PIN POSITION CALCULATORS
# ============================================================================

def esp32_pin(origin_x, origin_y, pin_num):
    """Get the connection point for an ESP32-C6-SuperMini pin."""
    # Left side pins 1-10: at (0, -(pin-1)*2.54) relative to origin
    # Right side pins 11-20: at (25.4, -(pin-11)*2.54) relative to origin
    if pin_num <= 10:
        return (origin_x, origin_y - (pin_num - 1) * 2.54)
    else:
        return (origin_x + 25.4, origin_y - (pin_num - 11) * 2.54)

def mini560_pin(origin_x, origin_y, pin_num):
    """Get connection point for Mini560 pin."""
    pins = {
        1: (0, 0), 2: (0, -2.54), 3: (0, -5.08), 4: (0, -7.62),
        5: (12.7, -25.4),
        6: (25.4, -7.62), 7: (25.4, -5.08), 8: (25.4, -2.54), 9: (25.4, 0)
    }
    dx, dy = pins[pin_num]
    return (origin_x + dx, origin_y + dy)

def sn65_pin(origin_x, origin_y, pin_num):
    """Get connection point for SN65HVD230DR pin."""
    pins = {
        1: (0, 0), 2: (0, -2.54), 3: (0, -5.08), 4: (0, -7.62),
        5: (27.94, 0), 6: (27.94, -2.54), 7: (27.94, -5.08), 8: (27.94, -7.62)
    }
    dx, dy = pins[pin_num]
    return (origin_x + dx, origin_y + dy)

def tlp290_pin(origin_x, origin_y, pin_num):
    """Get connection point for TLP290 pin.
    Pin 1 (Anode): left-top, Pin 2 (Cathode): left-bottom
    Pin 4 (Collector): right-top, Pin 3 (Emitter): right-bottom
    """
    pins = {
        1: (-7.62, 2.54), 2: (-7.62, -2.54),
        3: (7.62, -2.54), 4: (7.62, 2.54)
    }
    dx, dy = pins[pin_num]
    return (origin_x + dx, origin_y + dy)

def s8b_pin(origin_x, origin_y, pin_num):
    """Get connection point for S8B-XH-SM4-TB pin."""
    return (origin_x - 7.62, origin_y + 7.62 - (pin_num - 1) * 2.54)

def s4b_pin(origin_x, origin_y, pin_num):
    """Get connection point for S4B-XH-SM4-TB pin."""
    return (origin_x - 7.62, origin_y + 2.54 - (pin_num - 1) * 2.54)

def resistor_pin_h(origin_x, origin_y, pin_num):
    """Get connection point for a horizontal resistor (placed at 90°).
    When rotated 90°: pin 1 at left, pin 2 at right."""
    if pin_num == 1:
        return (origin_x - 3.81, origin_y)
    else:
        return (origin_x + 3.81, origin_y)

def resistor_pin_v(origin_x, origin_y, pin_num):
    """Get connection point for a vertical resistor (placed at 0°).
    Pin 1 at top, pin 2 at bottom."""
    if pin_num == 1:
        return (origin_x, origin_y - 3.81)  # top
    else:
        return (origin_x, origin_y + 3.81)  # bottom

def cap_pin_v(origin_x, origin_y, pin_num):
    """Get connection point for a vertical capacitor (placed at 0°).
    Pin 1 at top, pin 2 at bottom."""
    if pin_num == 1:
        return (origin_x, origin_y - 3.81)
    else:
        return (origin_x, origin_y + 3.81)


# ============================================================================
# MAIN SCHEMATIC GENERATION
# ============================================================================

def generate_schematic():
    output = []

    # ---- Component positions (A3 paper: 420x297mm) ----

    # Trailer Input Connector J2 (far left)
    j2_x, j2_y = 35.56, 99.06

    # Optocouplers (left-center), spaced 22.86mm vertically
    opto_x = 101.6  # center of TLP290 symbols
    opto_spacing = 22.86
    u3_x, u3_y = opto_x, 48.26    # L Turn
    u4_x, u4_y = opto_x, 71.12    # R Turn
    u5_x, u5_y = opto_x, 93.98    # Running Lights
    u6_x, u6_y = opto_x, 116.84   # Backup Lights

    # Current-limiting resistors (horizontal, to the left of optocouplers)
    # Placed so pin 2 connects directly to TLP290 anode (pin 1)
    r3_x, r3_y = u3_x - 7.62 - 3.81, u3_y + 2.54   # L Turn
    r4_x, r4_y = u4_x - 7.62 - 3.81, u4_y + 2.54   # R Turn
    r5_x, r5_y = u5_x - 7.62 - 3.81, u5_y + 2.54   # Running
    r6_x, r6_y = u6_x - 7.62 - 3.81, u6_y + 2.54   # Backup

    # Pull-up resistors (vertical, above optocoupler collectors)
    # Placed so pin 2 connects directly to TLP290 collector (pin 4)
    r7_x = u3_x + 7.62   # at collector x
    r7_y = u3_y + 2.54 + 3.81  # pin2 at collector, so center above
    r8_x = u4_x + 7.62
    r8_y = u4_y + 2.54 + 3.81
    r9_x = u5_x + 7.62
    r9_y = u5_y + 2.54 + 3.81
    r10_x = u6_x + 7.62
    r10_y = u6_y + 2.54 + 3.81

    # Voltage divider 1: Aux 12V sensing
    vd1_x = 73.66
    r11_x, r11_y = vd1_x, 147.32   # upper (100k), vertical
    r13_x, r13_y = vd1_x, 157.48   # lower (27k), vertical
    c1_x, c1_y = vd1_x + 10.16, 157.48  # filter cap, vertical

    # Voltage divider 2: Trailer Brakes sensing
    vd2_x = 73.66
    r12_x, r12_y = vd2_x, 180.34   # upper (100k), vertical
    r14_x, r14_y = vd2_x, 190.5    # lower (27k), vertical
    c2_x, c2_y = vd2_x + 10.16, 190.5   # filter cap, vertical

    # ESP32-C6 SuperMini (center)
    u1_x, u1_y = 195.58, 76.2

    # CAN transceiver SN65HVD230DR (right of center)
    ic1_x, ic1_y = 274.32, 76.2

    # RS pull-down resistor (vertical, near SN65HVD230DR RS pin)
    r1_x = ic1_x + 27.94   # at RS pin x
    r1_y = ic1_y - 7.62 + 3.81   # pin1 at RS, center below

    # CAN connector J1 (far right)
    j1_x, j1_y = 345.44, 76.2

    # Mini560 Buck Converter (bottom center)
    u2_x, u2_y = 195.58, 228.6

    # Mounting holes (bottom right)
    h1_x, h1_y = 335.28, 248.92
    h2_x, h2_y = 345.44, 248.92
    h3_x, h3_y = 355.6, 248.92
    h4_x, h4_y = 365.76, 248.92

    # ---- Build schematic content ----
    components = []
    wires = []
    labels = []
    power_syms = []
    no_connects = []
    junctions = []

    # ========== COMPONENTS ==========

    # --- J2: Trailer Input Connector (8-pin JST XH) ---
    components.append(make_component(
        "TrailCurrentSymbolLibrary:S8B-XH-SM4-TB", "J2",
        "Trailer_Input", "TrailCurrentFootprints:JST_S8B-XH-SM4-TB",
        j2_x, j2_y, 0, 8,
        ref_offset_x=-3, ref_offset_y=13, val_offset_x=-3, val_offset_y=-22
    ))

    # J2 pin assignments:
    # Pin 1: GND (trailer pin 1)
    # Pin 2: Trailer Brakes (trailer pin 2)
    # Pin 3: Tail/Running Lights (trailer pin 3)
    # Pin 4: Aux 12V+ (trailer pin 4)
    # Pin 5: R Turn/Stop (trailer pin 5)
    # Pin 6: Backup Lights (trailer pin 6)
    # Pin 7: L Turn/Stop (trailer pin 7)
    # Pin 8: GND (second ground return)

    # GND on J2 pins 1 and 8
    j2p1 = s8b_pin(j2_x, j2_y, 1)
    j2p8 = s8b_pin(j2_x, j2_y, 8)
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], j2p1[0], j2p1[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], j2p8[0], j2p8[1]))

    # Labels on J2 signal pins
    j2p2 = s8b_pin(j2_x, j2_y, 2)
    j2p3 = s8b_pin(j2_x, j2_y, 3)
    j2p4 = s8b_pin(j2_x, j2_y, 4)
    j2p5 = s8b_pin(j2_x, j2_y, 5)
    j2p6 = s8b_pin(j2_x, j2_y, 6)
    j2p7 = s8b_pin(j2_x, j2_y, 7)
    labels.append(make_global_label("BRAKE_12V", j2p2[0], j2p2[1], 180))
    labels.append(make_global_label("RUNNING_12V", j2p3[0], j2p3[1], 180))
    labels.append(make_global_label("AUX_12V_IN", j2p4[0], j2p4[1], 180))
    labels.append(make_global_label("R_TURN_12V", j2p5[0], j2p5[1], 180))
    labels.append(make_global_label("BACKUP_12V", j2p6[0], j2p6[1], 180))
    labels.append(make_global_label("L_TURN_12V", j2p7[0], j2p7[1], 180))

    # --- Optocoupler circuits (4 channels) ---
    opto_configs = [
        # (ref, opto_pos, rlimit_pos, rpullup_pos, signal_12v_label, gpio_label)
        ("U3", (u3_x, u3_y), (r3_x, r3_y), (r7_x, r7_y), "L_TURN_12V", "L_TURN"),
        ("U4", (u4_x, u4_y), (r4_x, r4_y), (r8_x, r8_y), "R_TURN_12V", "R_TURN"),
        ("U5", (u5_x, u5_y), (r5_x, r5_y), (r9_x, r9_y), "RUNNING_12V", "RUNNING"),
        ("U6", (u6_x, u6_y), (r6_x, r6_y), (r10_x, r10_y), "BACKUP_12V", "BACKUP"),
    ]
    r_limit_refs = ["R3", "R4", "R5", "R6"]
    r_pull_refs = ["R7", "R8", "R9", "R10"]

    for i, (opto_ref, opto_pos, rlimit_pos, rpull_pos, sig_label, gpio_label) in enumerate(opto_configs):
        ox, oy = opto_pos
        rx, ry = rlimit_pos
        px, py = rpull_pos

        # Place TLP290 optocoupler
        components.append(make_component(
            "Isolator:TLP290", opto_ref, "TLP290",
            "Package_SO:SOP-4_4.4x2.6mm_P1.27mm",
            ox, oy, 0, 4,
            ref_offset_x=-5, ref_offset_y=7, val_offset_x=0, val_offset_y=7
        ))

        # Place current-limiting resistor (horizontal, 90°)
        components.append(make_component(
            "Device:R", r_limit_refs[i], "2.2k",
            "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder",
            rx, ry, 90, 2,
            ref_offset_x=0, ref_offset_y=-3, val_offset_x=0, val_offset_y=3
        ))

        # Place pull-up resistor (vertical, 0°)
        components.append(make_component(
            "Device:R", r_pull_refs[i], "10k",
            "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder",
            px, py, 0, 2,
            ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
        ))

        # --- Wiring for this optocoupler channel ---

        # Anode pin (pin 1) of TLP290
        anode = tlp290_pin(ox, oy, 1)   # left-top
        cathode = tlp290_pin(ox, oy, 2) # left-bottom
        collector = tlp290_pin(ox, oy, 4) # right-top
        emitter = tlp290_pin(ox, oy, 3)  # right-bottom

        # Current-limiting resistor pin 2 → anode
        rl_p2 = resistor_pin_h(rx, ry, 2)  # right end of horizontal R
        # Wire from R pin 2 to anode if they don't perfectly align
        if abs(rl_p2[0] - anode[0]) > 0.01 or abs(rl_p2[1] - anode[1]) > 0.01:
            wires.append(make_wire(rl_p2[0], rl_p2[1], anode[0], anode[1]))

        # Signal label on current-limiting resistor pin 1 (input side)
        rl_p1 = resistor_pin_h(rx, ry, 1)  # left end
        labels.append(make_global_label(sig_label, rl_p1[0], rl_p1[1], 180))

        # GND on cathode (pin 2)
        power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], cathode[0], cathode[1]))

        # GND on emitter (pin 3)
        power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], emitter[0], emitter[1]))

        # Pull-up resistor: pin 2 (bottom) → collector
        rp_p2 = resistor_pin_v(px, py, 2)  # bottom of vertical R
        # Wire from pull-up R pin 2 to collector if not aligned
        if abs(rp_p2[0] - collector[0]) > 0.01 or abs(rp_p2[1] - collector[1]) > 0.01:
            wires.append(make_wire(rp_p2[0], rp_p2[1], collector[0], collector[1]))

        # +3.3V on pull-up resistor pin 1 (top)
        rp_p1 = resistor_pin_v(px, py, 1)  # top of vertical R
        power_syms.append(make_power_symbol("power", "+3.3V", pwr_counter[0], rp_p1[0], rp_p1[1]))

        # GPIO label on collector (extends right with short wire)
        labels.append(make_global_label(gpio_label, collector[0] + 5.08, collector[1], 0))
        wires.append(make_wire(collector[0], collector[1], collector[0] + 5.08, collector[1]))
        # Junction at collector where pull-up and GPIO label meet
        junctions.append(make_junction(collector[0], collector[1]))

    # --- Voltage Divider 1: Aux 12V sensing ---
    # R11 (100k, upper) - vertical
    components.append(make_component(
        "Device:R", "R11", "100k",
        "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder",
        r11_x, r11_y, 0, 2,
        ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
    ))
    # R13 (27k, lower) - vertical
    components.append(make_component(
        "Device:R", "R13", "27k",
        "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder",
        r13_x, r13_y, 0, 2,
        ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
    ))
    # C1 (100nF, filter) - vertical
    components.append(make_component(
        "Device:C", "C1", "100nF",
        "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
        c1_x, c1_y, 0, 2,
        ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
    ))

    # Wiring for VD1:
    r11_p1 = resistor_pin_v(r11_x, r11_y, 1)  # top - signal input
    r11_p2 = resistor_pin_v(r11_x, r11_y, 2)  # bottom - junction
    r13_p1 = resistor_pin_v(r13_x, r13_y, 1)  # top - junction
    r13_p2 = resistor_pin_v(r13_x, r13_y, 2)  # bottom - GND
    c1_p1 = cap_pin_v(c1_x, c1_y, 1)          # top - junction
    c1_p2 = cap_pin_v(c1_x, c1_y, 2)          # bottom - GND

    # Wire R11 bottom to R13 top (junction point)
    junction_y1 = r11_p2[1]
    wires.append(make_wire(r11_p2[0], r11_p2[1], r13_p1[0], r13_p1[1]))

    # Wire junction to C1 top (horizontal)
    wires.append(make_wire(r11_p2[0], r11_p2[1], c1_p1[0], c1_p1[1]))
    junctions.append(make_junction(r11_p2[0], r11_p2[1]))

    # Signal input label on R11 top
    labels.append(make_global_label("AUX_12V_IN", r11_p1[0], r11_p1[1], 90))

    # GND on R13 bottom and C1 bottom
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], r13_p2[0], r13_p2[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], c1_p2[0], c1_p2[1]))

    # ADC output label at junction
    labels.append(make_global_label("AUX_12V_SENSE", r11_p2[0] + 5.08, r11_p2[1], 0))
    wires.append(make_wire(r11_p2[0], r11_p2[1], r11_p2[0] + 5.08, r11_p2[1]))

    # --- Voltage Divider 2: Trailer Brakes sensing ---
    components.append(make_component(
        "Device:R", "R12", "100k",
        "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder",
        r12_x, r12_y, 0, 2,
        ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
    ))
    components.append(make_component(
        "Device:R", "R14", "27k",
        "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder",
        r14_x, r14_y, 0, 2,
        ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
    ))
    components.append(make_component(
        "Device:C", "C2", "100nF",
        "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
        c2_x, c2_y, 0, 2,
        ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
    ))

    r12_p1 = resistor_pin_v(r12_x, r12_y, 1)
    r12_p2 = resistor_pin_v(r12_x, r12_y, 2)
    r14_p1 = resistor_pin_v(r14_x, r14_y, 1)
    r14_p2 = resistor_pin_v(r14_x, r14_y, 2)
    c2_p1 = cap_pin_v(c2_x, c2_y, 1)
    c2_p2 = cap_pin_v(c2_x, c2_y, 2)

    wires.append(make_wire(r12_p2[0], r12_p2[1], r14_p1[0], r14_p1[1]))
    wires.append(make_wire(r12_p2[0], r12_p2[1], c2_p1[0], c2_p1[1]))
    junctions.append(make_junction(r12_p2[0], r12_p2[1]))

    labels.append(make_global_label("BRAKE_12V", r12_p1[0], r12_p1[1], 90))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], r14_p2[0], r14_p2[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], c2_p2[0], c2_p2[1]))

    labels.append(make_global_label("BRAKE_SENSE", r12_p2[0] + 5.08, r12_p2[1], 0))
    wires.append(make_wire(r12_p2[0], r12_p2[1], r12_p2[0] + 5.08, r12_p2[1]))

    # ========== ESP32-C6 SuperMini (U1) ==========
    components.append(make_component(
        "TrailCurrentSymbolLibrary:ESP32-C6-SuperMini", "U1",
        "ESP32-C6-SuperMini", "TrailCurrentFootprints:ESP32-C6-SuperMini_SMD",
        u1_x, u1_y, 0, 20,
        ref_offset_x=12, ref_offset_y=5, val_offset_x=12, val_offset_y=3
    ))

    # ESP32 pin connections via labels:
    # Pin 1 (TX) - no connect
    # Pin 2 (RX) - no connect
    # Pin 3 (GPIO0) - RUNNING (optocoupler output)
    # Pin 4 (GPIO1) - BACKUP (optocoupler output)
    # Pin 5 (GPIO2) - AUX_12V_SENSE (ADC)
    # Pin 6 (GPIO3) - L_TURN (optocoupler output)
    # Pin 7 (GPIO4) - R_TURN (optocoupler output)
    # Pin 8 (GPIO5) - BRAKE_SENSE (ADC)
    # Pin 9 (GPIO6) - no connect
    # Pin 10 (GPIO7) - no connect
    # Pin 11 (5V) - +5V
    # Pin 12 (GND) - GND
    # Pin 13 (3V3) - +3.3V
    # Pin 14 (GPIO20) - no connect
    # Pin 15 (GPIO19) - no connect
    # Pin 16 (GPIO18) - no connect
    # Pin 17 (GPIO15) - CAN_RX
    # Pin 18 (GPIO14) - CAN_TX
    # Pin 19 (GPIO9) - no connect
    # Pin 20 (GPIO8) - no connect (used internally for RGB LED)

    # Left side labels
    esp_p3 = esp32_pin(u1_x, u1_y, 3)
    esp_p4 = esp32_pin(u1_x, u1_y, 4)
    esp_p5 = esp32_pin(u1_x, u1_y, 5)
    esp_p6 = esp32_pin(u1_x, u1_y, 6)
    esp_p7 = esp32_pin(u1_x, u1_y, 7)
    esp_p8 = esp32_pin(u1_x, u1_y, 8)

    labels.append(make_global_label("RUNNING", esp_p3[0], esp_p3[1], 180))
    labels.append(make_global_label("BACKUP", esp_p4[0], esp_p4[1], 180))
    labels.append(make_global_label("AUX_12V_SENSE", esp_p5[0], esp_p5[1], 180))
    labels.append(make_global_label("L_TURN", esp_p6[0], esp_p6[1], 180))
    labels.append(make_global_label("R_TURN", esp_p7[0], esp_p7[1], 180))
    labels.append(make_global_label("BRAKE_SENSE", esp_p8[0], esp_p8[1], 180))

    # No connects on left side
    esp_p1 = esp32_pin(u1_x, u1_y, 1)
    esp_p2 = esp32_pin(u1_x, u1_y, 2)
    esp_p9 = esp32_pin(u1_x, u1_y, 9)
    esp_p10 = esp32_pin(u1_x, u1_y, 10)
    no_connects.append(make_no_connect(esp_p1[0], esp_p1[1]))
    no_connects.append(make_no_connect(esp_p2[0], esp_p2[1]))
    no_connects.append(make_no_connect(esp_p9[0], esp_p9[1]))
    no_connects.append(make_no_connect(esp_p10[0], esp_p10[1]))

    # Right side power
    esp_p11 = esp32_pin(u1_x, u1_y, 11)  # 5V
    esp_p12 = esp32_pin(u1_x, u1_y, 12)  # GND
    esp_p13 = esp32_pin(u1_x, u1_y, 13)  # 3V3
    power_syms.append(make_power_symbol("power", "+5V", pwr_counter[0], esp_p11[0], esp_p11[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], esp_p12[0], esp_p12[1]))
    power_syms.append(make_power_symbol("power", "+3.3V", pwr_counter[0], esp_p13[0], esp_p13[1]))

    # Right side labels
    esp_p17 = esp32_pin(u1_x, u1_y, 17)  # GPIO15 = CAN_RX
    esp_p18 = esp32_pin(u1_x, u1_y, 18)  # GPIO14 = CAN_TX
    labels.append(make_global_label("CAN_RX", esp_p17[0], esp_p17[1], 0))
    labels.append(make_global_label("CAN_TX", esp_p18[0], esp_p18[1], 0))

    # Right side no connects
    esp_p14 = esp32_pin(u1_x, u1_y, 14)  # GPIO20
    esp_p15 = esp32_pin(u1_x, u1_y, 15)  # GPIO19
    esp_p16 = esp32_pin(u1_x, u1_y, 16)  # GPIO18
    esp_p19 = esp32_pin(u1_x, u1_y, 19)  # GPIO9
    esp_p20 = esp32_pin(u1_x, u1_y, 20)  # GPIO8
    no_connects.append(make_no_connect(esp_p14[0], esp_p14[1]))
    no_connects.append(make_no_connect(esp_p15[0], esp_p15[1]))
    no_connects.append(make_no_connect(esp_p16[0], esp_p16[1]))
    no_connects.append(make_no_connect(esp_p19[0], esp_p19[1]))
    no_connects.append(make_no_connect(esp_p20[0], esp_p20[1]))

    # ========== CAN Transceiver (IC1) ==========
    components.append(make_component(
        "TrailCurrentSymbolLibrary:SN65HVD230DR", "IC1",
        "SN65HVD230DR", "TrailCurrentFootprints:SN65HVD230DR",
        ic1_x, ic1_y, 0, 8,
        ref_offset_x=14, ref_offset_y=10, val_offset_x=14, val_offset_y=8
    ))

    # IC1 pin connections:
    ic1_p1 = sn65_pin(ic1_x, ic1_y, 1)  # D (TXD)
    ic1_p2 = sn65_pin(ic1_x, ic1_y, 2)  # GND
    ic1_p3 = sn65_pin(ic1_x, ic1_y, 3)  # VCC
    ic1_p4 = sn65_pin(ic1_x, ic1_y, 4)  # R (RXD)
    ic1_p5 = sn65_pin(ic1_x, ic1_y, 5)  # VREF
    ic1_p6 = sn65_pin(ic1_x, ic1_y, 6)  # CANL
    ic1_p7 = sn65_pin(ic1_x, ic1_y, 7)  # CANH
    ic1_p8 = sn65_pin(ic1_x, ic1_y, 8)  # RS

    labels.append(make_global_label("CAN_TX", ic1_p1[0], ic1_p1[1], 180))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], ic1_p2[0], ic1_p2[1]))
    power_syms.append(make_power_symbol("power", "+3.3V", pwr_counter[0], ic1_p3[0], ic1_p3[1]))
    labels.append(make_global_label("CAN_RX", ic1_p4[0], ic1_p4[1], 180))
    no_connects.append(make_no_connect(ic1_p5[0], ic1_p5[1]))
    labels.append(make_global_label("CANL", ic1_p6[0], ic1_p6[1], 0))
    labels.append(make_global_label("CANH", ic1_p7[0], ic1_p7[1], 0))

    # RS pin → R1 (10k) → GND
    components.append(make_component(
        "Device:R", "R1", "10k",
        "Resistor_SMD:R_1206_3216Metric_Pad1.30x1.75mm_HandSolder",
        r1_x, r1_y, 0, 2,
        ref_offset_x=3, ref_offset_y=0, val_offset_x=3, val_offset_y=2
    ))
    r1_p1 = resistor_pin_v(r1_x, r1_y, 1)  # top → RS
    r1_p2 = resistor_pin_v(r1_x, r1_y, 2)  # bottom → GND
    wires.append(make_wire(ic1_p8[0], ic1_p8[1], r1_p1[0], r1_p1[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], r1_p2[0], r1_p2[1]))

    # ========== CAN Connector J1 (4-pin JST XH) ==========
    components.append(make_component(
        "TrailCurrentSymbolLibrary:S4B-XH-SM4-TB", "J1",
        "CAN_Bus", "TrailCurrentFootprints:JST_S4B-XH-SM4-TB",
        j1_x, j1_y, 0, 4,
        ref_offset_x=-3, ref_offset_y=8, val_offset_x=-3, val_offset_y=-12
    ))

    # J1 pin assignments (same as reference design):
    # Pin 1: GND
    # Pin 2: CANL
    # Pin 3: CANH
    # Pin 4: +12V
    j1p1 = s4b_pin(j1_x, j1_y, 1)
    j1p2 = s4b_pin(j1_x, j1_y, 2)
    j1p3 = s4b_pin(j1_x, j1_y, 3)
    j1p4 = s4b_pin(j1_x, j1_y, 4)
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], j1p1[0], j1p1[1]))
    labels.append(make_global_label("CANL", j1p2[0], j1p2[1], 180))
    labels.append(make_global_label("CANH", j1p3[0], j1p3[1], 180))
    power_syms.append(make_power_symbol("power", "+12V", pwr_counter[0], j1p4[0], j1p4[1]))

    # ========== Mini560 Buck Converter (U2) ==========
    components.append(make_component(
        "TrailCurrentSymbolLibrary:Mini560", "U2",
        "Mini560", "TrailCurrentFootprints:Mini560",
        u2_x, u2_y, 0, 9,
        ref_offset_x=12, ref_offset_y=5, val_offset_x=12, val_offset_y=3
    ))

    # Mini560 pin connections:
    m_p1 = mini560_pin(u2_x, u2_y, 1)   # VIN+
    m_p2 = mini560_pin(u2_x, u2_y, 2)   # VIN+
    m_p3 = mini560_pin(u2_x, u2_y, 3)   # GND
    m_p4 = mini560_pin(u2_x, u2_y, 4)   # GND
    m_p5 = mini560_pin(u2_x, u2_y, 5)   # EN
    m_p6 = mini560_pin(u2_x, u2_y, 6)   # GND
    m_p7 = mini560_pin(u2_x, u2_y, 7)   # GND
    m_p8 = mini560_pin(u2_x, u2_y, 8)   # VOUT+
    m_p9 = mini560_pin(u2_x, u2_y, 9)   # VOUT+

    power_syms.append(make_power_symbol("power", "+12V", pwr_counter[0], m_p1[0], m_p1[1]))
    power_syms.append(make_power_symbol("power", "+12V", pwr_counter[0], m_p2[0], m_p2[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], m_p3[0], m_p3[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], m_p4[0], m_p4[1]))
    no_connects.append(make_no_connect(m_p5[0], m_p5[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], m_p6[0], m_p6[1]))
    power_syms.append(make_power_symbol("power", "GND", pwr_counter[0], m_p7[0], m_p7[1]))
    power_syms.append(make_power_symbol("power", "+5V", pwr_counter[0], m_p8[0], m_p8[1]))
    power_syms.append(make_power_symbol("power", "+5V", pwr_counter[0], m_p9[0], m_p9[1]))

    # ========== Mounting Holes ==========
    components.append(make_mounting_hole("H1", h1_x, h1_y))
    components.append(make_mounting_hole("H2", h2_x, h2_y))
    components.append(make_mounting_hole("H3", h3_x, h3_y))
    components.append(make_mounting_hole("H4", h4_x, h4_y))

    # ========== Text annotations ==========
    texts = []
    texts.append(make_text("TrailCurrent Aftline", 25.4, 20.32, 3.81))
    texts.append(make_text("Signal Conditioning - Optocouplers (12V → 3.3V)", 60.96, 33.02, 2.0))
    texts.append(make_text("Voltage Dividers (12V → 3.0V ADC)", 55.88, 134.62, 2.0))
    texts.append(make_text("MCU", 200.66, 66.04, 2.0))
    texts.append(make_text("CAN Bus Interface", 269.24, 63.5, 2.0))
    texts.append(make_text("Power Supply (12V → 5V)", 190.5, 218.44, 2.0))

    # ========== ASSEMBLE SCHEMATIC ==========
    sch = f"""(kicad_sch
\t(version 20250114)
\t(generator "eeschema")
\t(generator_version "9.0")
\t(uuid "{ROOT_UUID}")
\t(paper "A3")
{LIB_SYMBOLS}
"""
    # Add all elements
    for c in components:
        sch += c
    for w in wires:
        sch += w
    for l in labels:
        sch += l
    for p in power_syms:
        sch += p
    for n in no_connects:
        sch += n
    for j in junctions:
        sch += j
    for t in texts:
        sch += t

    sch += f"""\t(sheet_instances
\t\t(path "/"
\t\t\t(page "1")
\t\t)
\t)
\t(embedded_fonts no)
)
"""
    return sch


if __name__ == "__main__":
    schematic = generate_schematic()
    output_dir = os.path.join(os.path.dirname(__file__),
                              "TrailCurrentAftline")
    output_path = os.path.join(output_dir,
                               "TrailCurrentAftline.kicad_sch")
    with open(output_path, 'w') as f:
        f.write(schematic)
    print(f"Schematic written to: {output_path}")
    print(f"Components placed: U1 (ESP32-C6), U2 (Mini560), U3-U6 (TLP290 x4), IC1 (SN65HVD230DR)")
    print(f"Resistors: R1 (10k CAN RS), R3-R6 (2.2k current limit), R7-R10 (10k pull-up), R11-R12 (100k), R13-R14 (27k)")
    print(f"Capacitors: C1-C2 (100nF filter)")
    print(f"Connectors: J1 (CAN 4-pin), J2 (Trailer 8-pin)")
    print(f"Mounting holes: H1-H4")
