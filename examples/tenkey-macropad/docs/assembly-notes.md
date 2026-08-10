# Rev A assembly notes

1. Verify the release SHA-256 manifest, exact BOM MPNs, stencil revision, and GCT USB4085 drawing before material release.
2. Inspect incoming boards for outline, M2 holes, USB edge/overhang geometry, connector PTH drills, mask registration, and exposed 5 V/GND test pads.
3. Apply paste and reflow the **underside only**. All SMT—including D1–D10, U1, U2, protection, passives, crystal, reset, and test pads—is on B.Cu. J1 is not in the SMT CPL. **Diode cathode/pad 1 is the square/marked pad toward ROW0/ROW1.** AOI all ten polarities.
4. Observe U1 pin 1, U2 orientation, Y1, and SW11 orientation. R1/R2 must each be 5.1 kΩ; R3/R4 must each be 22 Ω. There is no front-side SMT reflow operation.
5. Install GCT `USB4085-GF-A` J1 from the underside and wave/selective/manual solder all signal and shell pins. Inspect for full barrel fill, bridges, opens, connector seating, and shell retention. JLCPCB lists this part as `C7095263`; confirm the assembly preview and process before ordering.
6. Before other THT installation, perform continuity/short tests and program/identify U1 through J2 when practical.
7. Fit J2 from the underside with pin 1 matching the assembly drawing. Fit CHERRY MX switches SW1–SW10 from the front/user side only after underside inspection; avoid forcing bent pins.
8. Clean only with processes compatible with the switches and connector. Do not wash unsealed switches unless their supplier process explicitly permits it.
9. TP1 is +5 V; TP2 is GND. They are bare probe pads and have no purchased BOM items.
10. Keycaps, USB cable, programmer, screws, plate, and enclosure are not included.

All substitutions require review of rating, package drawing, pad geometry, polarity, lifecycle, and the relevant functional calculation. No BOM substitution is pre-approved.
