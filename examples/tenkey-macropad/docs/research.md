# TenKeyMacroPad design research and verification basis

Status: design input reconciled to the final Rev A records; not a fabrication sign-off  
Prepared: 2026-08-09  
Target: a new, bus-powered, ten-key USB-C macro pad derived conceptually from the existing ATmega32U4 four-key design

## 1. Scope and evidence policy

This document records the electrical basis that the schematic, PCB, firmware, and release checks must implement. It deliberately separates four levels of evidence:

1. **Normative/primary requirements:** USB-IF specifications and Microchip device documentation.
2. **Manufacturer implementation guidance:** Microchip application notes, ST protection-device documentation, connector drawings, and JLCPCB capabilities.
3. **Working reference hardware:** Arduino and SparkFun production designs. These are useful cross-checks, but their circuits must not override the MCU or USB specifications.
4. **Secondary/community education:** QMK's firmware documentation is primary for QMK behavior; AI03 and individual keyboard projects are secondary for general PCB practice.

Passing ERC and DRC proves internal consistency against encoded CAD rules. It does **not** prove USB compliance, correct fuse/bootloader programming, assembled component identity, solder quality, or physical operation. Final functional evidence requires an assembled-board test described in section 12.

## 2. Proposed architecture and why

| Block | Design decision | Reason and source |
|---|---|---|
| MCU | ATmega32U4-AU, TQFP-44, 5 V, 16 MHz | It provides native USB device hardware and enough GPIO for a 2×5 matrix. Microchip rates 16 MHz operation in the 4.5–5.5 V region; the device datasheet's typical 5 V bus-powered USB implementation directly supports this architecture. See datasheet sections 1, 6, 21.3, 21.4, and 29. |
| USB role | USB 2.0 upstream-facing peripheral/sink; no USB-PD | A macro pad is a USB device, not a host or power source. A sink receptacle independently terminates CC1 and CC2 with Rd. USB Type-C specification R2.0 sections 2.3 and 4.5.2.2.3.1. |
| Connector | USB-C 16-contact USB-2-only receptacle | Provides reversible D+/D− and does not populate unused SuperSpeed lanes. Exact manufacturer part must be selected before assigning its footprint. |
| Power | Bus-powered 5 V rail; no 3.3 V regulator required | The ATmega32U4 bus-powered 5 V application connects the USB supply to the device's VCC/AVCC/UVCC/VBUS requirements. Keep the design below declared/default USB current. |
| Clock | External 16 MHz crystal plus calculated load capacitors | ATmega32U4 full-speed USB requires an external crystal oscillator or external source clock; crystal-less operation is only specified for low speed. Datasheet sections 6.3 and 21.4. |
| Matrix | Two rows × five columns, ten switches, one diode per switch | Seven GPIO instead of ten; per-key diodes prevent ghost paths. QMK documents both the electrical scan and the required diode-direction declaration. |
| Programming | Standard 2×3 AVR ISP header plus reset button/test point | A blank MCU has no bootloader. ISP gives a guaranteed recovery/programming path for flash, fuses, and bootloader. Microchip AN2519 section 4 and the ATmega32U4 datasheet section 28.8. |
| Protection | Low-capacitance two-line USB ESD array next to connector; protected VBUS input | The connector is user-accessible. The MCU datasheet explicitly permits transient/ESD suppressors; ST's USBLC6-2 is intended for USB 2.0 and its layout guidance requires short I/O, VBUS, and ground paths. |

The recommended GPIO allocation is deliberately separate from USB and ISP:

- Columns: PB4, PB5, PB6, PC6, PD7 (`B4`, `B5`, `B6`, `C6`, `D7` in QMK).
- Rows: PD0, PD1 (`D0`, `D1` in QMK).
- ISP remains PB1/SCK, PB2/PDI/MOSI, PB3/PDO/MISO, RESET, VCC, and GND.
- PE2/HWB remains available for bootloader recovery rather than being consumed by the matrix.
- PF4, PF5, PF7 are avoided because they overlap the JTAG interface and the device ships with JTAG enabled according to the datasheet; using them would add a fuse/software dependency.

This pin plan is not complete until the schematic symbol pin numbers and the QMK configuration are checked against each other.

## 3. ATmega32U4 required circuit

Primary source: Microchip, **ATmega16U4/ATmega32U4 Datasheet**, Atmel-7766J, April 2016, accessed 2026-08-09: [PDF](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf), [product page](https://www.microchip.com/en-us/product/atmega32u4).

Additional manufacturer guidance: Microchip, **AN2519 AVR Microcontroller Hardware Design Considerations**, revision B, accessed 2026-08-10: [PDF](https://www.microchip.com/content/dam/mchp/documents/MCU08/ApplicationNotes/ApplicationNotes/AN2519-AVR-Microcontroller-Hardware-Design-Considerations-00002519B.pdf).

### 3.1 Supply pins and capacitors

The schematic must account for every supply and ground pin on the TQFP-44 symbol:

- Every VCC pin connects to the 5 V bus-powered rail.
- Every ordinary GND pin connects to GND; do not assume stacked power pins are internally interchangeable in the schematic.
- UVCC connects to the 5 V rail; it is the USB pad regulator input.
- UGND connects to GND.
- Every AVCC pin must connect to VCC even if the ADC is unused. The datasheet section 2.2.17 allows direct connection when the ADC is unused and calls for a low-pass filter when it is used.
- VBUS is the USB VBUS monitor input and connects to protected connector VBUS in the bus-powered application.
- UCAP is the internal USB regulator output. It is **not** a general-purpose power rail. Connect exactly 1 µF, ±10%, from UCAP to GND as required by sections 2.2.12 and 21.5.
- AREF receives a local 100 nF capacitor to GND if it is not externally driven. Do not connect AREF directly to VCC; the datasheet describes it as the ADC reference input and permits only a capacitive load when using the internal reference.
- Place at least one 100 nF ceramic decoupler at each MCU supply/ground pair, with the capacitor in the local high-current loop rather than reached through a long plane path. AN2519 section 2 says a decoupler is essential for every supply/ground pair and must be physically close.
- The ATmega32U4 USB design guidelines highly recommend 10 µF on VBUS (datasheet section 21.5). Rev A deliberately uses 4.7 µF plus the local 100 nF capacitors to retain attach/inrush margin; this adaptation is recorded in `engineering-calculations.md` and requires measured inrush and steady-state acceptance. Check actual capacitance under 5 V DC bias, not only the printed nominal value.

Suggested minimum capacitor accounting for review:

| Ref function | Nominal | Required check |
|---|---:|---|
| UCAP | 1 µF, ±10% | Direct UCAP-to-GND, short, not shared as a supply |
| VBUS bulk | 4.7 µF on Rev A | Deliberate departure from the highly recommended 10 µF; measure capacitance/inrush and respect USB attach behavior |
| VCC decoupling | 100 nF per supply pair | One at each relevant MCU supply location |
| AVCC decoupling | 100 nF | Local to AVCC; optional bead/filter only if its DC drop and ADC needs are analyzed |
| AREF | 100 nF | AREF-to-GND, no external reference in this design |

### 3.2 USB data pins

The ATmega32U4 datasheet section 2.2.8/2.2.9 and section 21.5 require:

- D− connector path to MCU D− through a **22 Ω ±5%** series resistor.
- D+ connector path to MCU D+ through a **22 Ω ±5%** series resistor.
- Both traces short, same-length as practical, adjacent/parallel through the route, and without accumulated vias.

The 22 Ω resistors are not the USB-C CC resistors. They serve the MCU's USB data interface and must not be replaced by generic 27 Ω or omitted merely because a reference board differs.

Route order should be:

`USB-C receptacle -> ESD array placed at connector -> coupled D+/D− route -> 22 Ω series resistors -> MCU D+/D−`

The ESD part should use flow-through routing where its pinout permits it. Avoid branch stubs at the connector's doubled D pins and at the protection device.

### 3.3 Clock

- Use a 16 MHz crystal between XTAL1 and XTAL2.
- Place the crystal and its capacitors next to the MCU, with short, symmetric paths and a quiet ground return.
- Datasheet section 6.3 says C1 and C2 should be equal; the recommended range for an 8–16 MHz crystal oscillator is 12–22 pF, but the optimum depends on the selected crystal's specified load capacitance and PCB/pin stray capacitance.
- Select the crystal first, then calculate/validate C1 and C2. For equal capacitors, use the starting relationship `CL ~= C1*C2/(C1+C2) + Cstray`; do not copy 22 pF blindly.
- Full-speed USB cannot rely on the internal RC oscillator. Datasheet section 21.4 explicitly limits crystal-less operation to USB low speed.
- Firmware, fuse values, and QMK `F_CPU` must all agree with 16 MHz.

### 3.4 Reset, HWB, and programming

- RESET is active-low. Fit a reset switch to GND and an external pull-up; 10 kΩ is a practical value compatible with debug/programming guidance. The device itself has a 30–60 kΩ internal reset pull-up, but AN2519 recommends an external pull-up for robustness.
- A large reset capacitor can interfere with some debug/programming interfaces. If fitted, verify it against the selected programmer. A simple keyboard board can omit it and rely on the reset button plus internal filtering unless a documented noise requirement justifies it.
- Expose PE2/HWB as a pad or boot switch if Atmel DFU hardware boot entry is desired. Datasheet sections 10.3.4 and 27.5.3 say HWB must be low during the external reset edge and the HWBE fuse must be programmed for this behavior.
- Always expose the standard AVR ISP signals. For ATmega32U4 serial programming, PB2 is PDI/MOSI, PB3 is PDO/MISO, PB1 is SCK, plus RESET, VCC/VTG, and GND (datasheet table 28-14).
- Standard 6-pin AVR ISP header mapping is: pin 1 MISO, pin 2 VTG/VCC, pin 3 SCK, pin 4 MOSI, pin 5 RESET, pin 6 GND. See Microchip [AVR Programming Adapter DS50003533](https://ww1.microchip.com/downloads/aemDocuments/documents/DEV/ProductDocuments/UserGuides/50003533.pdf), section 2.1, accessed 2026-08-09.
- Mark pin 1 in copper/silkscreen and keep the header mechanically accessible after enclosure assembly.
- Do not claim USB bootloader operation until a specific bootloader, fuse set, USB VID/PID policy, and initial ISP programming procedure are recorded.

## 4. USB-C USB-2 peripheral wiring

Primary source used for specific pin and Rd clauses: USB-IF, **USB Type-C Cable and Connector Specification Release 2.0**, August 2019, accessed 2026-08-09: [PDF](https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019_0.pdf). Relevant locations: section 2.3; receptacle pin table 3-1; section 4.5.2.2.3.1; table 4-25.

The current USB-IF library lists **USB Type-C Release 2.5, March 2026**. Recheck the final design against that current release before production: [official specification page](https://www.usb.org/usb-type-cr-cable-and-connector-specification), [document library](https://www.usb.org/documents?search=usb+type+c).

The Release 2.0 clause numbers retained below are historical design evidence,
not current sign-off evidence. Revalidate the pin and Rd requirements against
Release 2.5 and record its current table/section identifiers before production.

For a USB-2-only receptacle:

| Receptacle contacts | Connection |
|---|---|
| A6 and B6 | Join locally into one D+ net; join without a long branch/stub |
| A7 and B7 | Join locally into one D− net; join without a long branch/stub |
| A5 / CC1 | Its own 5.1 kΩ Rd to GND |
| B5 / CC2 | A separate 5.1 kΩ Rd to GND |
| A4, A9, B4, B9 | All connector VBUS contacts joined to protected VBUS |
| A1, A12, B1, B12 | All ground-return contacts joined to board GND |
| SBU1/SBU2 | No connect for this USB-2-only peripheral; explicitly mark NC |
| Shell | Tie according to the documented enclosure/EMC strategy; never confuse shell pins with the four signal-ground contacts |

Both CC resistors are mandatory and independent. A single 5.1 kΩ on one CC pin works in only one cable orientation or fails with some C-to-C sources. Release 2.0 section 4.5.2.2.3.1 states that both CC1 and CC2 are independently terminated to ground through Rd; table 4-25 gives Rd as 5.1 kΩ nominal (±20% functional tolerance). Use 1% parts for ordinary BOM consistency.

This is a sink/UFP implementation:

- It never drives VBUS or VCONN.
- It does not implement USB Power Delivery.
- It consumes only default USB current and declares a truthful maximum current in its USB descriptors/QMK configuration.
- VBUS powers the board after source attachment. A resettable fuse or appropriately rated input protection can be placed in series with the board's 5 V load, but the MCU VBUS sense and ESD topology must still match their data sheets.

The current base USB 2.0 specification package is listed by USB-IF as updated 2025-06-03: [official USB 2.0 specification page](https://www.usb.org/document-library/usb-20-specification). USB compliance ultimately depends on the USB 2.0 electrical and protocol requirements, not merely Type-C pin wiring.

## 5. ESD and connector protection

Selected reference option: STMicroelectronics USBLC6-2SC6, SOT-23-6.

Primary source: STMicroelectronics, **USBLC6-2 Very Low Capacitance ESD Protection**, DS4260 Rev 7, December 2021, accessed 2026-08-09: [datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf), [product page and CAD/SPICE resources](https://www.st.com/en/protections-and-emi-filters/usblc6-2.html).

Why it is a defensible option:

- It is specified for two USB 2.0 data lines up to 480 Mb/s.
- It protects VBUS as part of its rail-to-rail structure.
- Maximum I/O-to-GND capacitance is 3.5 pF and the data-channel matching is specified.
- It is rated to IEC 61000-4-2 level 4 at device level (8 kV contact, 15 kV air).
- Its datasheet section 2.3 requires the data, VBUS, and ground paths to be as short as possible and says to place the protection device as close as possible to the disturbance source, normally the connector.

Selection caveats:

- Verify that the exact orderable suffix and SOT-23-6 pinout match KiCad's `Power_Protection:USBLC6-2SC6` symbol and `Package_TO_SOT_SMD:SOT-23-6` footprint.
- Do not substitute a high-capacitance general TVS without checking USB data loading.
- ESD component presence is not sufficient: connector-to-array distance and especially the array's ground inductance determine protection effectiveness.
- If a different protection array is chosen for JLCPCB availability, use that manufacturer's schematic and layout, then redo symbol/footprint/pin-map checks.

Texas Instruments' **ESD and Surge Protection for USB Interfaces**, SLVAF82B, revised January 2024, is a useful independent manufacturer cross-check. It recommends at least 3.3 V working voltage and less than 4 pF capacitance for USB 2.0 data-line protectors, plus IEC 61000-4-2 ratings of at least 8 kV contact/15 kV air: [PDF](https://www.ti.com/lit/an/slvaf82b/slvaf82b.pdf).

## 6. Ten-key matrix and firmware contract

QMK is the primary source for QMK's own scanning/configuration behavior:

- [How a Keyboard Matrix Works](https://docs.qmk.fm/how_a_matrix_works), accessed 2026-08-09.
- [Adding Your Keyboard to QMK](https://docs.qmk.fm/porting_your_keyboard_to_qmk), matrix configuration section, accessed 2026-08-09.
- [Configuring QMK](https://docs.qmk.fm/config_options), hardware options, accessed 2026-08-09.

### 6.1 Electrical orientation

Use `COL2ROW`:

`column GPIO -> switch -> diode anode -> diode cathode/banded end -> row GPIO`

For the standard KiCad `Device:D` convention and common SOD-123 switching diodes, pin 2 is anode and pin 1 is cathode. The cathode mark must face the row. Confirm this again against the exact chosen diode's data sheet and footprint marking.

Each one of the ten switches gets its own diode. All diodes face the same direction. A 2×5 electrical matrix then uses seven MCU pins and prevents the ghost path that appears when three corners of a rectangle are pressed.

### 6.2 QMK configuration that must match the schematic

Example contract for the proposed pins:

```json
{
  "processor": "atmega32u4",
  "bootloader": "atmel-dfu",
  "diode_direction": "COL2ROW",
  "matrix_pins": {
    "cols": ["B4", "B5", "B6", "C6", "D7"],
    "rows": ["D0", "D1"]
  }
}
```

The `bootloader` line is a release choice, not an electrical fact. If Caterina is selected instead, the build configuration, fuse values, flash size, reset/entry behavior, and flashing instructions must change together. The ISP header remains required for first programming and recovery either way.

The physical `LAYOUT_ortho_2x5` mapping must explicitly map keys K1–K5 to row 0/columns 0–4 and K6–K10 to row 1/columns 0–4. Firmware compile success alone does not prove this mapping; compare every switch reference and net in the schematic to the JSON matrix, then perform the physical test in section 12.

QMK's hardware configuration defines `COL2ROW` as the black/cathode mark facing the rows. Its data-driven configuration infers the matrix size from the row/column arrays. QMK also exposes a maximum USB current setting; set this to the measured/worst-case board load rather than leaving an unjustified 500 mA declaration.

## 7. Working reference schematics and CAD

### 7.1 Manufacturer/official reference designs

1. **Microchip ATmega32U4 datasheet, Figure 21-3** — the controlling reference circuit for a 5 V bus-powered ATmega32U4. Use it for UVCC, VBUS, UCAP, D+/D− resistors, and clock requirements. It is not a complete product schematic and does not include USB-C CC wiring.
2. **Arduino Leonardo** — a production ATmega32U4, 16 MHz native-USB board with official schematic and CAD. Its connector is Micro-USB, so it validates the MCU/clock/reset/ISP patterns but not USB-C CC circuitry. [Product documentation](https://docs.arduino.cc/hardware/leonardo/), [schematic PDF](https://docs.arduino.cc/resources/schematics/A000057-schematics.pdf), [CAD ZIP](https://docs.arduino.cc/static/fd50e8f3be44a3217bbfd5d123295bdf/A000057-cad-files.zip). Accessed 2026-08-09.
3. **SparkFun Qwiic Pro Micro USB-C (ATmega32U4), hardware version 2.0** — a shipped 5 V/16 MHz ATmega32U4 USB-C design with downloadable schematic and Eagle files. It is an implementation cross-check for a USB-C 32U4 board, not a normative source. [Hookup guide/resources](https://learn.sparkfun.com/tutorials/qwiic-pro-micro-usb-c-atmega32u4-hookup-guide/resources-and-going-further), [schematic PDF](https://cdn.sparkfun.com/assets/4/4/f/2/a/Qwiic_Pro_Micro_V2_0_USB_C_Schematic.pdf). Accessed 2026-08-09.
4. **ST USBLC6-2** — official protection IC application diagram, package drawing, SPICE model, and CAD symbol/footprint downloads are linked from the product page above.

For every copied circuit fragment, the review record must name the source figure and list intentional differences. A board being sold or published does not prove every detail is best practice, nor does it guarantee compatibility with a different connector, stack-up, bootloader, or firmware.

### 7.2 Secondary/community references

- [AI03 PCB Design Guide](https://wiki.ai03.com/books/pcb-design), accessed 2026-08-09. Useful for keyboard-oriented design workflow and visual explanations. It is secondary educational material; its site warns that portions may be outdated/incomplete, so any electrical value must be traced back to a current manufacturer or specification.
- Public QMK keyboard directories are useful for firmware-layout examples, but they are community contributions. Treat them as a searchable corpus, not verified reference circuits.

## 8. KiCad 10 standard symbols and footprints

The following were confirmed in the locally installed KiCad 10 standard libraries on 2026-08-09. Official source repositories: [KiCad symbols](https://gitlab.com/kicad/libraries/kicad-symbols/), [KiCad footprints](https://gitlab.com/kicad/libraries/kicad-footprints/).

| Function | Standard symbol | Candidate standard footprint | Release rule |
|---|---|---|---|
| MCU | `MCU_Microchip_ATmega:ATmega32U4-A` | `Package_QFP:TQFP-44_10x10mm_P0.8mm` | Symbol includes this default footprint and Microchip datasheet; still compare every pin and package code to ATmega32U4-AU. |
| USB-C | `Connector:USB_C_Receptacle_USB2.0_16P` | `Connector_USB:USB_C_Receptacle_GCT_USB4085` | Release part is GCT `USB4085-GF-A`, JLCPCB/LCSC `C7095263`. Verify pads against the [GCT drawing](https://gct.co/files/drawings/usb4085.pdf). |
| USB ESD | `Power_Protection:USBLC6-2SC6` | `Package_TO_SOT_SMD:SOT-23-6` | Cross-check ST top-view pin numbering; do not swap I/O and rail pins. |
| Switches | `Switch:SW_Push` | `Button_Switch_Keyboard:SW_Cherry_MX_1.00u_PCB` | Use PCB-mount MX only if the selected mechanical switch and plate/enclosure match it; do not assume hot-swap support. |
| Matrix diode | `Device:D` | Candidate `Diode_SMD:D_SOD-123` | Exact diode package/order code controls footprint; pin 1 cathode, pin 2 anode must match the data sheet. |
| Crystal | `Device:Crystal` or 4-pad crystal symbol | Exact manufacturer land pattern | Do not choose a generic 3225 footprint until the exact crystal pad drawing is selected. |
| ISP | `Connector_Generic:Conn_02x03_Odd_Even` | `Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical` | Verify odd/even numbering produces the AVR ISP mapping; prefer a keyed/shrouded variant if space permits. |

KiCad library membership does not certify that a footprint matches a distributor listing. The exact manufacturer part number, drawing revision, pad dimensions, body courtyard, shell stakes, and orientation must be reconciled before release.

## 9. USB routing constraints

The ATmega32U4 data sheet provides the device-specific routing rule: short, same-length, near each other, and avoid via accumulation. Translate that into explicit board constraints:

- Route D+ and D− as one coupled pair from the connector through ESD and series resistors to the MCU.
- Keep both on the same copper layer for the principal run.
- Maintain constant pair spacing and width except for the shortest necessary pad escapes.
- Keep the route over an uninterrupted GND reference. Do not cross a split, plane edge, void, or slot.
- Do not route unrelated copper between the pair.
- Avoid vias; if unavoidable, use the same number and geometry in both members and provide a nearby return-path GND via when changing reference layer.
- Do not use length-tuning serpentine simply to produce an attractive numerical match if it breaks coupling. Coupled geometry and a continuous return path have priority; a short 12 Mb/s path should not need elaborate meanders.
- Place the 22 Ω resistors symmetrically and close to the MCU USB pins. Place the ESD array at the connector.
- Record routed length and skew, but also visually/algorithmically check parallel overlap, width, gap, via count, reference plane, and branch/stub length.

The nominal USB interconnect is commonly designed around a 90 Ω differential environment. The Type-C R2.0 cable section 3.7.1 recommends 90 Ω ±5 Ω for the raw cable differential pair, but a PCB impedance claim must be based on the actual PCB stack-up and fabricator process—not copied from a cable requirement or guessed from trace width.

## 10. JLCPCB two-layer constraints and impedance-claim limit

Primary current source: JLCPCB [PCB Manufacturing Capabilities](https://jlcpcb.com/capabilities/Capabilities), accessed 2026-08-09.

For ordinary 1 oz, one- or two-layer boards, JLCPCB currently lists:

- Minimum track width/spacing: 0.10/0.10 mm (4/4 mil).
- Track-width tolerance: ±20%.
- Recommended two-layer 1 oz PTH annular ring: 0.25 mm or larger; absolute minimum 0.18 mm.
- Pad-to-track clearance: 0.10 mm minimum, with advice to stay above the minimum.
- PTH-to-track clearance: 0.35 mm recommended, 0.28 mm minimum.

These are manufacturing minima, not preferred design rules. The project should use comfortable values unless a specific footprint escape forces tighter geometry.

JLCPCB's capabilities table currently lists its **controlled impedance** service for 4, 6, 8, and higher layer counts, not two layers. Its [controlled-impedance stack-up page](https://jlcpcb.com/impedance) is explicitly for multilayer controlled-impedance boards. Therefore:

- A normal two-layer order may use a field-solver estimate for USB pair geometry, but the project must not label the result “fabricator-controlled 90 Ω.”
- A two-layer 1.6 mm board has a distant opposite-layer reference and large process/material uncertainty. A ground pour is not equivalent to a close, continuous internal reference plane.
- JLCPCB itself describes two-layer signal/signal construction as having only basic, limited impedance control in its [impedance-routing guidance](https://jlcpcb.com/blog/impedance-controlled-routing).
- If an accountable controlled-impedance claim is required, change the project to an offered four-layer stack-up, choose it before routing, compute the pair with JLCPCB's [impedance calculator](https://jlcpcb.com/pcb-impedance-calculator), encode the resulting width/gap, order impedance control, and archive the selected stack-up.

For this compact full-speed (12 Mb/s) macro pad, a carefully routed short pair on two layers may function well, but that is an engineering expectation to be verified on hardware—not a controlled-impedance manufacturing guarantee.

## 11. Pre-release design evidence

The new KiCad project should contain, at minimum:

1. `docs/research.md` — this source basis.
2. A requirements/constraint table naming each critical net class and its source.
3. A pin-map ledger: MCU physical pin, symbol pin, net, firmware name, and matrix coordinate.
4. A BOM with manufacturer part number, package, tolerance/rating, and footprint for every critical component.
5. ERC report with zero errors and every warning explained.
6. DRC report with zero errors, zero unconnected items, and every warning explained.
7. Connectivity audit counts: ten switches, ten matrix diodes, two rows, five columns, two CC resistors, all MCU power/ground pins, UCAP capacitor, crystal network, USB resistors, ESD array, and six ISP signals.
8. USB pair audit: net names, length, skew, width, gap, coupled length, via count, same-layer check, and uninterrupted GND reference.
9. Filled-zone audit and rendered top/bottom copper images; no reliance on unfilled zone outlines.
10. Schematic PDF, PCB renders, 3D views, and Gerber/drill plots inspected independently of the editable KiCad view.
11. QMK source and a successful clean compile for the exact MCU, clock, bootloader, matrix pins, diode direction, and layout.
12. Fabrication-readiness review against the exact JLCPCB order parameters and exact assembly parts.

No search result or reference schematic may be copied without recording:

- exact source and revision;
- device/package identity;
- operating voltage and clock;
- copied circuit boundary;
- differences introduced in this project;
- schematic/ERC/netlist evidence that the intended connections exist;
- PCB evidence that placement/routing-dependent requirements were implemented.

## 12. What “verified working” must mean

### 12.1 Checks possible before fabrication

- KiCad opens and parses the schematic and PCB without repair warnings.
- ERC and DRC meet the gates in section 11.
- Schematic-to-PCB netlist and footprint counts agree.
- USB-C A/B orientation connections, independent CC pull-downs, ESD topology, 22 Ω resistors, UCAP, supplies, clock, reset, and ISP are all explicitly audited.
- QMK compiles for the exact configuration and produces a firmware image within flash limits.
- Gerbers and drill files are visually inspected; copper zones are filled in the exported result.
- BOM and placement exports map to the same exact part/footprint revisions.

These support the statement **“design checks pass and the board is ready for prototype fabrication.”** They do not support **“the board works.”**

### 12.2 Required prototype bring-up

1. Unpowered continuity/short test: 5 V-to-GND resistance, USB D+/D− not shorted, CC1/CC2 each approximately 5.1 kΩ to GND, all ground pins continuous.
2. Current-limited first power from a USB current meter/lab setup; check 5 V and UCAP voltage and watch for heating.
3. Program fuses and bootloader through ISP; read them back and archive the command/output.
4. Confirm 16 MHz clock operation where practical.
5. Enumerate with both a USB-A-to-C cable and a standards-compliant C-to-C cable in both plug orientations.
6. Record VID/PID, descriptors, configured current, and repeated connect/disconnect behavior on at least two host types if possible.
7. Exercise reset, bootloader entry, ISP recovery, and firmware reflash.
8. Run a matrix test that presses and releases every key individually, then every three-key rectangle combination relevant to ghosting, then all ten keys as supported by firmware.
9. Confirm each physical key reports the intended matrix coordinate/keycode; archive the test log.
10. Perform ESD, signal-integrity, suspend/resume, and USB compliance testing appropriate to the intended product claim. USB-IF notes that official electrical assessment uses its approved compliance tools/procedures: [USB electrical test resources](https://www.usb.org/sites/default/files/electrical_tests).

Only after these tests pass can the prototype reasonably be described as functionally verified. Formal USB compliance or a production guarantee requires the applicable compliance program, not only successful enumeration.

## 13. Official files to download and archive

Create a `references/` manifest containing URL, download date, revision, SHA-256, and license/redistribution note for each file. Recommended official downloads:

1. [ATmega16U4/32U4 datasheet, Atmel-7766J PDF](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7766-8-bit-AVR-ATmega16U4-32U4_Datasheet.pdf).
2. [Microchip AN2519 revision B hardware-design application note PDF](https://www.microchip.com/content/dam/mchp/documents/MCU08/ApplicationNotes/ApplicationNotes/AN2519-AVR-Microcontroller-Hardware-Design-Considerations-00002519B.pdf).
3. [USB Type-C R2.0 August 2019 PDF snapshot](https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019_0.pdf) plus the current [USB Type-C specification package](https://www.usb.org/usb-type-cr-cable-and-connector-specification).
4. Current [USB 2.0 specification package](https://www.usb.org/document-library/usb-20-specification).
5. [ST USBLC6-2 datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf) and the CAD/SPICE resources from its [product page](https://www.st.com/en/protections-and-emi-filters/usblc6-2.html).
6. [Arduino Leonardo schematic](https://docs.arduino.cc/resources/schematics/A000057-schematics.pdf) and [CAD ZIP](https://docs.arduino.cc/static/fd50e8f3be44a3217bbfd5d123295bdf/A000057-cad-files.zip).
7. [SparkFun Qwiic Pro Micro USB-C schematic](https://cdn.sparkfun.com/assets/4/4/f/2/a/Qwiic_Pro_Micro_V2_0_USB_C_Schematic.pdf) and Eagle files linked from the [official resources page](https://learn.sparkfun.com/tutorials/qwiic-pro-micro-usb-c-atmega32u4-hookup-guide/resources-and-going-further).
8. Exact USB-C connector manufacturer's drawing and STEP model: release part GCT `USB4085-GF-A`; use the [USB4085 drawing](https://gct.co/files/drawings/usb4085.pdf), [official product page](https://gct.co/connector/usb4085), and KiCad's matching package model.
9. Exact crystal and matrix-diode manufacturer data sheets after those orderable parts are selected.
10. A pinned QMK source revision from the [official QMK repository](https://github.com/qmk/qmk_firmware) used to compile the release firmware.

USB-IF specifications have specific license terms. Archive them for internal design evidence but do not assume they can be redistributed with a public project. The project should normally commit a manifest and source links/hashes rather than republishing restricted specification packages.

## 14. Unresolved choices that must be closed before sign-off

- Revalidate GCT `USB4085-GF-A` / JLCPCB `C7095263` stock and THT assembly-process availability at order time.
- Exact ESD array order code and assembly availability.
- Exact 16 MHz crystal, load capacitance, ESR, tolerance, and matching capacitor calculation.
- Exact matrix diode and package.
- PCB-mount versus plate-mount versus hot-swap switches and corresponding mechanical design.
- 2-layer “short, carefully referenced pair” versus 4-layer fabricator-controlled impedance.
- Atmel DFU versus Caterina bootloader; fuse bytes and first-programming method.
- USB VID/PID and product strings appropriate to prototype versus distribution.
- Shell-to-ground/chassis strategy based on the actual enclosure and EMC target.
- Required mounting holes, key pitch, connector retention, board thickness, and enclosure clearances.

Until these are resolved, the project can be a well-founded prototype design but not a fully accounted manufacturing release.
