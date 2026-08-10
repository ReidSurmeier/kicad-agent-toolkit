# Design study and evidence pack

Complete this gate before schematic capture, placement, routing, substitution,
or material redesign.

## Source authority by scope

Use the source that owns the question rather than one total ranking:

- Applicable law, safety, EMC, and interface standards control compliance claims.
- Exact-part datasheets, errata, package drawings, and manufacturer checklists
  control component implementation.
- The selected fabricator/assembler's quoted stackup and process rules control
  producibility.
- Exact-family application notes and evaluation boards guide implementation.
- Version-matched KiCad documentation controls what the tool checks and exports.
- IPC standards control only their named design, fabrication, assembly, or
  acceptance scope.
- Textbooks explain physics and judgment; community designs provide examples.

Record revision, URL, access date, section/page, and operating assumptions.
Resolve conflicts within the controlling scope; leave the decision blocked when
two applicable controlling sources remain inconsistent.

## Required artifacts

- Requirements: rails/ranges, continuous and peak current, interfaces and edge
  rates, firmware/clock mode, environment, EMC/ESD/safety, mechanics, assembly,
  manufacturer options, cost/stackup, and test strategy.
- Pin maps: package pad, symbol pin, function/type, intended net/domain, startup
  state, and unused disposition for every critical or custom device.
- Circuit evidence: function/limits, controlling source sections, official
  implementation, adaptations, calculations/ratings, firmware dependencies,
  and `verified`, `conditional`, or `unresolved` state for each block.
- Power/clock calculations: rail budget, voltage drop/current capacity,
  transient/inrush, decoupling loops, regulator stability, oscillator load/ESR/
  drive/startup, and thermal limits.
- Manufacturing basis: exact stackup, copper, impedance service, drill/via,
  line/space, mask, edge, assembly limits, and deliberate margin above minima.
- Verification and bring-up plan: checks, renders, output inspection, numerical
  bench limits, fixtures, and responsibility for acceptance.

## Critical-net matrix

Create a row for each interface, clock, power path, sensitive analog path,
switching node, isolation boundary, or other critical group. Record exact nets
and endpoints, electrical intent, geometry, matching, placement order/limits,
return/protection, sources/calculations, KiCad enforcement, and manual checks.

For metrics, retain tool/version, endpoints, units, pad/via treatment, breakout
and stub treatment, coupling threshold, and raw output. “Looks parallel” and one
total-length value are not reproducible evidence.

For each plane net, derive the expected pad set from the authoritative netlist.
Specify intended direct/thermal attachments, then report every pad as zone-direct,
zone-thermal, trace/via-only, or missing, with islands and bottleneck widths.

## Reference circuits

Prefer official evaluation boards and licensed open hardware with editable
sources. Store immutable revision, license, device/package, stackup, production
status, errata, claimed validation, and extracted pattern. Keep two-layer and
controlled-impedance multilayer examples in separate cohorts. Revalidate every
pattern against the current exact-part and production sources.

The gate passes when the evidence explains the intended schematic and layout.
Carry every unresolved item forward by name.
