# PCB design curriculum for an agent

The objective is not to memorize generic rules. It is to build a traceable model
of the specific circuit, physical implementation, production process, and tests
before making irreversible design choices.

## 1. Requirements and architecture

Define supplies and limits, load/current cases, clocks and firmware, interfaces
and edge rates, environment, EMC/ESD/safety category, mechanics, assembly,
production volume, manufacturer options, programming, and functional tests.
Draw the power tree, data paths, reset/boot states, fault paths, and trust/safety
boundaries. Completion means every block has an explicit input/output contract.

## 2. Exact components and circuits

Build exact-package pin maps. For each circuit block, record the controlling
datasheet/errata sections, official working implementation when available,
adaptations, calculations, ratings/derating, firmware dependencies, and open
questions. A searched schematic becomes a candidate until this comparison is
complete.

## 3. Power, signal, and return paths

Calculate rail current, transient demand, voltage drop, copper/via capacity,
regulator stability, decoupling loops, clock load/startup, and thermal limits.
For every critical interface define topology, endpoints, width/gap/impedance,
reference, via/stub/uncoupled budget, protection, and placement order. Analyze
the return path at every point, especially layer and plane-reference changes.

## 4. Production constraints

Select the actual stackup and assembly process. Record copper, drills, annular
rings, line/space, mask/paste, edge, impedance, material, panel, component-side,
and THT/reflow/selective/manual constraints with margin above absolute minima.
Validate every critical/custom footprint against the exact package drawing and
assembler process.

## 5. KiCad encoding

Make the schematic the topology source. Encode netclasses, custom constraints,
clearance/creepage, copper-to-edge, differential limits, via counts, and zone
behavior where KiCad supports them. Name every manual inspection that remains.
Place by mechanical and current/signal-flow constraints, then route critical
loops/interfaces before power and ordinary signals.

## 6. Verification ladder

1. Netlist and exact pin-map agreement.
2. Whole-project ERC plus visual schematic review.
3. Saved source hashes and clean-process schematic parity/DRC.
4. Critical-net metrics with reproducible measurement definitions.
5. Filled-plane expected-pad reconciliation and island/neck review.
6. Copper, mask, paste, silkscreen, outline, drills, and 3D inspection.
7. Fresh Gerber/drill/BOM/CPL generation and independent parsing.
8. Manufacturer DFM and assembly-preview reconciliation.
9. Current-limited bring-up, programming, interfaces, all-I/O, thermal, fault,
   and soak tests with numerical pass/fail criteria.

Each rung answers a narrower question. Higher rungs do not retroactively prove
the assumptions at lower ones, and CAD checks never replace the physical rung.

## 7. Learning corpus

Start with exact-part and official sources. Add textbooks to explain fields,
transmission lines, return current, decoupling, EMC, and power integrity. Add
official evaluation boards and licensed open hardware for concrete patterns.
Classify every item by authority, revision, license, hardware cohort, and claimed
validation. Extract hypotheses, then revalidate them for the current project.

See `docs/sources/comparison.md` for the claim-by-claim audit and
`docs/sources/corpus-policy.md` for redistribution rules.
