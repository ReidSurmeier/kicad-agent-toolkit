# Prototype P001 bring-up and acceptance plan

**Status: not executed.** Completing CAD, ERC, DRC, firmware compilation, or fabrication-output checks is not a hardware pass.

## Equipment

Current-limited 5 V supply/USB power monitor, DMM, oscilloscope with suitable USB probing if needed, known-good USB-A-to-C and USB-C-to-C cables/hosts, AVR ISP programmer, ESD-safe fixture, and logged host USB enumeration tools.

## Sequence and acceptance

1. Visual/AOI: exact BOM, diode polarity, U1/U2/J1 orientation, no bridges, complete J1 PTH barrel fill, correct board revision. **Pass:** zero unresolved discrepancy.
2. Unpowered resistance: discharge the board, then measure VBUS_RAW–GND and +5V–GND after the reading settles for 10 s; diode-test protection paths without overstressing USB pins. **Decision:** below 100 Ω is a stop; 100 Ω–1 kΩ requires fault-path analysis before power; above 1 kΩ permits the next step but is not proof of correctness. Record both polarities, actual values, settling behavior, and instrument.
3. First power from a regulated 5.00 V source current-limited to 50 mA. Raise the limit only after rail behavior is understood and never above the firmware's 100 mA declaration during this test. **Pass:** +5 V remains 4.75–5.25 V at the board, steady current is below 100 mA, no component rises more than 15 °C above ambient during the first 10 minutes, and the protection does not cycle. Capture inrush separately with bandwidth sufficient for the applicable USB test; a handheld current meter cannot close that requirement.
4. ISP identity/recovery: read signature and fuses without writing. **Pass:** ATmega32U4 signature and documented fuse decision. Do not write fuses until commands/image are independently checked.
5. Bootloader/application: install the pinned Atmel DFU bootloader/fuses through ISP only if required, then flash the release QMK HEX. **Pass:** readback/hash or documented verify succeeds and ISP remains recoverable.
6. USB-A-to-C enumeration. **Pass:** stable HID enumeration with intended prototype VID/PID/product, zero disconnect/re-enumeration events during a 10-minute idle plus active-key interval, and measured steady current below 100 mA.
7. USB-C-to-C in both plug orientations. **Pass:** stable enumeration and identical key behavior in both orientations. Test at least two known-good cables/ports.
8. Keys: actuate all ten individually and in matrix combinations. **Pass:** F13–F22 mapping exactly once per press, no stuck/missed key, and no ghosting for all required simultaneous combinations.
9. Reset/DFU: SW11 resets; tap Key 10 gives F22; hold Key 10 and press Key 1 enters DFU. **Pass:** all behaviors and ISP recovery work repeatedly.
10. Signal/clock debug if enumeration is marginal: verify the oscillator is 16 MHz within the selected crystal/MCU tolerance and startup requirement using a low-capacitance probing method; compare UCAP after regulator enable and reset timing against the exact ATmega32U4 datasheet limits. Inspect D+/D− with a USB-compliant fixture if electrical quality is in question. UCAP may be 0 V immediately after ordinary reset while `UVREGE` is disabled.
11. Soak/reconnect: 100 plug/enumerate cycles and at least one-hour powered key test. **Pass:** zero unexplained disconnects, zero key errors, steady current remains below 100 mA, and no component exceeds the 15 °C-above-ambient investigation threshold.

Archive prototype serial, board/firmware hashes, host/cable IDs, instruments/calibration, raw logs, photos, current/voltage measurements, failures and corrective actions. Only then may claim level move to `prototype-tested`.
