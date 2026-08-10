# Rev A mechanical contract

All coordinates are millimetres in the KiCad board datum.

- Finished outline: `(2,2)`, `(103,2)`, `(103,75)`, `(2,75)`; **101 × 73 mm**.
- M2 NPTH holes: diameter 2.2 mm at `(5,5)`, `(100,5)`, `(5,72)`, `(100,72)`.
- Key centers, row 0: `(14,38)`, `(33.05,38)`, `(52.10,38)`, `(71.15,38)`, `(90.20,38)`.
- Key centers, row 1: `(14,57.05)`, `(33.05,57.05)`, `(52.10,57.05)`, `(71.15,57.05)`, `(90.20,57.05)`.
- Key pitch: 19.05 mm horizontally and vertically; footprints are 1.00u PCB-mount CHERRY MX.
- USB-C J1 datum/footprint origin: `(52,7)`, rotation 0°, **underside/B.Cu**; connector body overhang follows the archived GCT/KiCad model.
- Reset center `(78,10)`; ISP header center `(90,10)`; TP1 `(97.5,8)`; TP2 `(99,14)`, all on the underside.
- Front/user side population is exactly SW1–SW10. Every diode and every other populated electrical component is on the underside; H1–H4 are side-neutral mechanical holes.
- Component heights and USB mating geometry must be checked from the STEP model/drawing against any future enclosure. No enclosure, plate cutout, or keycap envelope is released with Rev A.

The generated STEP and 1:1 assembly PDFs are the exchange files; this Markdown ledger is a cross-check, not a substitute for dimension inspection.
