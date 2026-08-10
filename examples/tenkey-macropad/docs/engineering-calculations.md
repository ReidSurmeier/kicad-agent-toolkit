# Rev A engineering calculations and budgets

## USB load and protection

The application USB descriptor declares 100 mA. A conservative pre-prototype allocation is 40 mA MCU/USB activity, 2 mA CC and bias paths, 3 mA leakage/miscellaneous, and 25 mA engineering margin: **70 mA budget**, with no LEDs or other powered loads. This is below the 100 mA descriptor and 250 mA PPTC hold rating. It is a design budget, not a measurement; P001 bring-up must record inrush and steady current.

C10 is 4.7 µF ±10% X7R. Six 100 nF supply/reference capacitors contribute 0.6 µF nominal on +5 V; nominal direct +5 V capacitance is about 5.3 µF and worst tolerance remains below 10 µF before DC-bias derating. C3 is on UCAP, not directly across VBUS. This change from the earlier 10 µF placeholder preserves USB attach/inrush margin. Actual capacitance and inrush must be measured.

The exact PPTC is Littelfuse `1206L025YR`: 250 mA hold-rated at the datasheet's reference conditions. Its hold/trip behavior, resistance, voltage drop, and temperature dependence make it fault-current limiting rather than precision overcurrent protection. USBLC6-2SC6 is placed between connector and series resistors with short ground/power returns. Each CC pin has its own 5.1 kΩ Rd.

## Crystal load

The exact crystal is ABM8-16.000MHZ-12-D2Y-T with 12 pF specified load. With equal 18 pF C0G capacitors:

`CL ≈ (C1 × C2) / (C1 + C2) + Cstray = 9 pF + 3 pF = 12 pF`.

The 3 pF stray term is an explicit board/pin/package estimate. Five-percent capacitors give a nominal switched-cap contribution of 8.55–9.45 pF before stray uncertainty. P001 must verify reliable start-up over intended voltage/temperature; a measured mismatch requires capacitor reassessment, not arbitrary tuning.

## Routing/rules

- Default signal width/clearance: 0.20/0.20 mm.
- +5V and VBUS_RAW width: 0.381 mm minimum; selected for robust low-current distribution rather than an ampacity limit.
- General vias: 0.60/0.30 mm; power vias 0.70/0.35 mm where used.
- USB full-speed copper paths are under 16 mm per connector orientation. Measured supplemental path skew is at most about 1.01 mm connector-to-ESD, 0.08 mm ESD-to-series, and 2.0 mm series-to-MCU. KiCad's scoped pair rules remain authoritative.
- A two-layer 1.6 mm board with 0.20/0.20 mm geometry is **not claimed as controlled 90 Ω differential impedance**. Short full-speed routing and continuous ground reference are the design basis.

## Mechanical

Outline 101 × 73 mm; four 2.2 mm M2 holes have 3 mm center-to-edge distance. Keys are on a 19.05 mm grid. Enclosure/plate fit is outside Rev A and remains unclaimed.
