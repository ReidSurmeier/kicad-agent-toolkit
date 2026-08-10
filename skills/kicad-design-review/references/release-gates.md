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
For an assembly order, upload the exact BOM/CPL/package and reconcile the
manufacturer preview for reference, package, side, rotation, polarity, DNP,
origin, and process before granting assembly readiness. A fabrication-only
release may mark this preview `not applicable`; it is not assembly-ready.

The bundled `pcb-agent release` profile is explicitly a JLCPCB-style two-layer
package and requires a project `.kibot.yaml` for its default cross-environment
gate. Do not present its `*-JLCPCB.zip` as a profile for another manufacturer.
For another process, create and test a manufacturer-specific KiBot/output
profile or report the neutral native exports as incomplete pending that work.
`--skip-container` omits independent KiBot evidence and cannot support the full
pipeline claim.

## Physical test

The bring-up plan names fixtures and numerical pass/fail limits for shorts,
current, rails, clock, programming, firmware, interfaces, I/O, thermals, and
fault recovery. This gate remains `not executed` until hardware measurements
exist; design checks cannot close it.

## Verdict

- `ready`: every pre-fabrication gate has current evidence and no unaccepted
  blocker/major risk.
- `ready with accepted risks`: every required gate passes, no blocker or major
  risk remains, and only explicit, owned, accepted minor risks or limitations
  remain.
- `not ready`: controlling evidence is missing, checks are stale/failed, or a
  blocker or major risk remains. Calling a major risk “accepted” does not change
  this verdict.

Report fabrication readiness and functional verification as separate verdicts.
