# Release gates

## Source

The reviewed revision is immutable by commit or hashes; all sheets and board
files parse/render; no loaded or divergent edit session remains; requirements,
source revisions, constraints, production basis, and verification plan are
archived.

## Electrical

Whole-project ERC is dispositioned; critical net-to-pin mappings and exact
symbol-to-footprint maps are independently verified; every circuit block is
traced to controlling sources and validated adaptations.

## Layout

Zones are freshly filled; unrouted items are zero or accepted by name; DRC is
clean or every exclusion is owned; critical metrics reconcile with renders;
mechanical, clearance/creepage, return, thermal, test, and assembly checks pass.
The authoritative clean-process command evidence is tied to the source hash.

## Manufacturing

Outputs are regenerated from the reviewed source and parsed independently.
Gerber/drill layers, outline, holes, mask, paste, legend, BOM, CPL, side,
rotation, origin, component process, and manufacturer options are reconciled.

## Physical test

The bring-up plan names fixtures and numerical pass/fail limits for shorts,
current, rails, clock, programming, firmware, interfaces, I/O, thermals, and
fault recovery. This gate remains `not executed` until hardware measurements
exist; design checks cannot close it.

## Verdict

- `ready`: every pre-fabrication gate has current evidence and no unaccepted
  blocker/major risk.
- `ready with accepted risks`: all required gates pass except explicit, owned,
  accepted risks.
- `not ready`: controlling evidence is missing, checks are stale/failed, or a
  blocker/major risk remains.

Report fabrication readiness and functional verification as separate verdicts.
