# TenKey macropad evidence fixture

This directory contains the sanitized KiCad source and engineering records used
to exercise the toolkit. It is a design-checks-passed case study, not a certified
reference design or proof of assembled hardware.

- `source/`: KiCad project, project rules, jobset, KiBot configuration, and local
  custom footprint.
- `docs/`: requirements research, calculations, decisions, assembly/fabrication
  notes, verification record, and the unexecuted bring-up plan.
- `design/`: machine-readable request, evidence, and firmware pin contract.
- `qa/`: release-gate contract.

The USB-C connector is GCT USB4085-GF-A, a through-hole part requiring a later
THT soldering step. All SMT is on the underside; the ten MX switches mount from
the user side.
