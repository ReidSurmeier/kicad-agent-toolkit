# TenKeyMacroPad design decisions

This is the project-specific evidence record. Normative facts, current links,
and reference-design comparisons are expanded in [research.md](research.md).

## Functional contract

- Ten MX-compatible switches in a 2-row × 5-column matrix.
- ATmega32U4-AU at 5 V and 16 MHz; native USB 2.0 full-speed device.
- USB-C receptacle used as a USB 2.0 sink/device only; no USB-PD controller.
- QMK `COL2ROW`: switch → diode anode; diode band/cathode → row.
- AVR ISP header, reset button, +5 V/GND test points, four M2 mounting holes.

## MCU and matrix pin map

| Function | Net | ATmega32U4 pin | QMK name |
|---|---|---:|---|
| Row 0 | `ROW0` | 18, PD0 | `D0` |
| Row 1 | `ROW1` | 19, PD1 | `D1` |
| Column 0 | `COL0` | 28, PB4 | `B4` |
| Column 1 | `COL1` | 29, PB5 | `B5` |
| Column 2 | `COL2` | 30, PB6 | `B6` |
| Column 3 | `COL3` | 31, PC6 | `C6` |
| Column 4 | `COL4` | 27, PD7 | `D7` |

USB remains on D− pin 3 and D+ pin 4. ISP uses PB1/SCK, PB2/MOSI, and PB3/MISO.
The selected matrix pins avoid USB, ISP, reset, crystal, power, and the JTAG
pins that would otherwise complicate first-boot firmware.

## USB-C circuit

- Exact connector: GCT `USB4085-GF-A`, using KiCad's matching
  `Connector_USB:USB_C_Receptacle_GCT_USB4085` through-hole footprint.
- The PTH VBUS contacts escape to ordinary external vias. This removes the
  former USB4105 via-in-pad/VIPPO requirement and allows ordinary JLCPCB board
  fabrication; J1 itself still needs a THT/wave-selective/manual assembly step.
- A6/B6 are locally joined as D+; A7/B7 are locally joined as D−.
- CC1 and CC2 each have their own 5.1 kΩ pull-down. They are not tied together.
- USBLC6-2SC6 is placed between the connector and 22 Ω series resistors.
- D+/D− are kept together through the long connector-to-ESD run. Short
  connector and protection-device fan-outs are necessarily uncoupled.
- The connector-to-ESD route is checked from both plug-orientation pin pairs;
  the generated structural audit records the measured paths and enforces the
  encoded 4 mm maximum skew.
- The board uses 0.20 mm data traces and a nominal 0.20 mm pair gap, with a
  0.15 mm compact-breakout minimum encoded in the custom rules.

The ATmega32U4 datasheet explicitly calls for 22 Ω series resistors on D+ and
D− and a 1 µF UCAP capacitor. See the [Microchip datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf).
The independent 5.1 kΩ CC pull-downs implement the USB-C sink/device attach
contract; see the [USB-IF Type-C specification page](https://www.usb.org/usb-type-cr-cable-and-connector-specification).

## Power, clock, and reset

- VBUS enters through Littelfuse `1206L025YR`, a 250 mA hold-rated PPTC at its
  specified reference conditions. +5 V and the routed VBUS feed
  use at least 0.381 mm (15 mil) copper.
- Every VCC/UVCC/AVCC pin and every GND/UGND pin is present in the schematic.
- Six 100 nF supply/reference capacitors, one 4.7 µF bulk capacitor, and
  1 µF on UCAP are included.
- The 16 MHz crystal uses two 18 pF C0G load capacitors and a short local loop.
- RESET has a 10 kΩ pull-up, pushbutton to ground, and ISP connection.

Microchip's hardware-design guidance is the basis for local decoupling and
short crystal routing: [AN2519](https://www.microchip.com/content/dam/mchp/documents/MCU08/ApplicationNotes/ApplicationNotes/AN2519-AVR-Microcontroller-Hardware-Design-Considerations-00002519B.pdf).

## PCB and fabrication reasoning

- GND pours exist and are filled on both F.Cu and B.Cu. Targeted stitching vias
  join local islands; KiCad connectivity reports zero named-net open edges.
- Front/user-side population is exactly SW1–SW10. Matrix diodes and every
  other populated electrical component have their bodies on the underside.
  SMT uses one underside reflow; J1 and J2 require a later THT operation. All
  routed copper is unlocked/editable.
- Four board-only M2 holes are excluded from BOM and position output.
- This is a two-layer board. JLCPCB's current controlled-impedance offerings
  are for multilayer stackups, so the USB pair is **not** claimed as a
  fabricator-controlled 90 Ω differential structure. For a compliance-grade
  impedance claim, migrate to a selected four-layer JLC stackup and recalculate
  width/gap before routing. See [JLCPCB capabilities](https://jlcpcb.com/capabilities/Capabilities)
  and [controlled impedance](https://jlcpcb.com/impedance).

## Reference-design cross-checks

- Arduino Leonardo validates the 5 V/16 MHz ATmega32U4 clock, reset, power, and
  ISP pattern, but uses Micro-USB: [official schematic](https://docs.arduino.cc/resources/schematics/A000057-schematics.pdf)
  and [CAD archive](https://docs.arduino.cc/static/fd50e8f3be44a3217bbfd5d123295bdf/A000057-cad-files.zip).
- SparkFun's shipped Qwiic Pro Micro USB-C provides an independent USB-C/32U4
  implementation comparison: [official resource page](https://learn.sparkfun.com/tutorials/qwiic-pro-micro-usb-c-atmega32u4-hookup-guide/resources-and-going-further)
  and [schematic](https://cdn.sparkfun.com/assets/4/4/f/2/a/Qwiic_Pro_Micro_V2_0_USB_C_Schematic.pdf).
- QMK's matrix documentation defines the selected `COL2ROW` diode orientation:
  [How a Keyboard Matrix Works](https://docs.qmk.fm/how_a_matrix_works).
