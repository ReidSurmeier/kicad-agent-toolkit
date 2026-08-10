# Portable KiCad/PCB agent curriculum: evidence audit and repository blueprint

Prepared: 2026-08-10  
Audited inputs: `docs/pcb-knowledge/source-map.md` and `TenKeyMacroPad-BSide/docs/*.md`  
Scope: circuit design, grounding and return paths, power integrity, USB 2.0/USB Type-C, EMC/ESD, DFM/assembly, verification limits, and prototype bring-up

## Executive assessment

The local knowledge is a strong basis for a **low-voltage, two-layer, USB 2.0 full-speed microcontroller board**. Its best features are the evidence hierarchy, explicit release gates, package/pin-map checks, return-path language, generated-output inspection, and refusal to call unbuilt hardware “working.” These agree with current USB-IF, Microchip, KiCad, IPC, IEC, vendor, and textbook guidance.

It is not yet a portable general PCB curriculum. Several statements are device-, PHY-, fabricator-, stack-up-, or KiCad-version-specific but are written close to general rules. The corpus is also thin on power-distribution-network analysis, EMC planning and pre-compliance, assembly acceptance, measurement uncertainty, thermal/reliability design, and non-USB circuit families. A coordinator skill should route each design into domain-specific branches instead of teaching macro-pad patterns as universal PCB rules.

The highest-priority corrections are:

1. The audit found internal ledger drift: 18 pF versus 22 pF crystal capacitors, “500 mA fuse” versus “250 mA PPTC hold rating,” proposed versus implemented matrix pin maps, and obsolete document revisions. The sanitized fixture in this repository now normalizes the populated values, exact PPTC, and final pin map; revisioned source checks remain a continuing gate.
2. Replace rank-only conflict resolution with **authority by claim and scope**. A fabricator controls what it will build; USB-IF controls USB interface requirements; a component datasheet controls that component; law and the applicable product standard control market access and safety.
3. Treat the short two-layer USB route as a documented prototype tradeoff, not as an exception to the USB impedance target or as a reusable geometry.
4. Add system-level EMC/ESD gates. A TVS diode’s component test rating and clean CAD checks do not establish product immunity or emissions compliance.
5. Separate volatile facts and copyrighted source material from stable agent procedure. Commit skills, original summaries, manifests, hashes, fixtures, and tests; keep restricted standards and textbooks link-only.

## Audit method and confidence

Claims were compared against the most specific current first-party source available as of the preparation date. Official specifications, regulator pages, component data, KiCad documentation, and fabricator capabilities were treated as controlling only inside their stated scope. Manufacturer application notes and official reference designs were used as implementation evidence. Textbooks were used to test whether the local heuristics reflect durable engineering models; they do not override a current normative or device-specific requirement.

The audit does not reproduce restricted standards or textbook passages. Section and table identifiers should be revalidated from the licensed/current document at design time because standards, web documentation, and supplier capabilities change.

## Source hierarchy for the portable corpus

Do not resolve conflicts by a single global ladder. First classify the claim, then use the authority that owns that claim.

| Priority within its scope | Source class | Controls | Portable-corpus treatment |
|---|---|---|---|
| 0 | Applicable law, regulatory regime, safety/product standard, customer/environmental requirements | Whether and under what conditions a product may be built, shipped, or used | Metadata and links; licensed copy outside Git unless redistribution is expressly allowed |
| 1 | Current interface specification and compliance program | USB electrical/protocol/connector requirements and what “compliant” or logo-eligible means | Link, revision, date, hash, and clause pointers; do not republish USB-IF packages by default |
| 1 | Exact orderable component datasheet, errata, package drawing, and manufacturer checklist | Pins, limits, required passives, layout-sensitive circuits, package geometry, programming and startup | Link, revision, date, hash; local extracted claims must cite sections |
| 1 | Contracted fabricator/assembler capability and accepted order configuration | What that supplier agrees to manufacture/assemble for that order | Snapshot the chosen parameters and access date; revalidate at order time |
| 2 | Manufacturer application note and official evaluation/reference design | Defensible implementation patterns for a named device/family and operating condition | Record differences; never silently generalize across devices or PHYs |
| 2 | EDA documentation for the pinned release and file format | What ERC, DRC, routers, exporters, and CLI checks actually do | Pin KiCad version; link to versioned docs, not only `master` |
| 3 | IPC/IEC/ANSI and other industry standards outside the directly controlling interface | Generic design, fabrication, assembly, test, and EMC methods | Bibliographic record and licensed clause pointers; no unlicensed normative text |
| 4 | Authoritative textbooks and peer-reviewed engineering literature | Durable models: current loops, transmission lines, PDNs, EMC coupling, measurement | Bibliographic citations and original summaries only |
| 5 | Shipped open hardware, community guides, forums, and tutorials | Examples, vocabulary, failure hypotheses, and workflow ideas | Require an explicit license and trace every electrical rule upward |

Conflict procedure:

1. State the exact claim, operating conditions, product jurisdiction, and design revision.
2. Identify the source that owns that claim; recency breaks ties only among sources with equivalent authority and scope.
3. Record whether the conflict is a real contradiction, a different operating condition, or a design choice inside an allowed range.
4. Resolve the project ledger and its machine-checkable rule together. An unresolved controlling conflict blocks the affected release gate.

## Claim-to-source map

| Topic / reusable claim | Best controlling or corroborating source | Audit of local material | Skill rule |
|---|---|---|---|
| Exact symbol-pin-to-footprint-pad mapping is essential; ERC depends on configured electrical types | [ATmega32U4 product/data sheet](https://www.microchip.com/en-us/product/atmega32u4); [KiCad 10 Schematic Editor](https://docs.kicad.org/10.0/en/eeschema/eeschema.html) | Agrees. The pin-table and independent footprint check are excellent gates. | Require exact MPN/package and a generated pin/pad ledger before schematic sign-off. |
| A clean ERC does not prove circuit function | [KiCad 10 Schematic Editor](https://docs.kicad.org/10.0/en/eeschema/eeschema.html) | Agrees. Local language properly limits the claim. | Test ERC behavior with intentionally wrong-value and wrong-pin fixtures that ERC cannot catch. |
| AVR supply pairs need local low-inductance decoupling; resonator selection/layout is device-specific | [Microchip AN2519, revision B](https://www.microchip.com/content/dam/mchp/documents/MCU08/ApplicationNotes/ApplicationNotes/AN2519-AVR-Microcontroller-Hardware-Design-Considerations-00002519B.pdf) | Agrees, but some links point to revision A and the project has conflicting crystal capacitor values. | Cite revision B/current product documentation; calculate from the exact crystal and keep one populated-value ledger. |
| Trace current capacity is not set by a universal width | [IPC-2152 scope/TOC](https://www.ipc.org/TOC/IPC-2152.pdf); [IPC design standards index](https://www.ipc.org/ipc-design-standards) | Agrees. The 0.381 mm power width is correctly called a project choice, not an ampacity law. | Require current, copper, temperature-rise, voltage-drop, length, ambient, planes, and vias as inputs; label estimates and standard/tool revision. |
| A PDN must be designed for transient current and impedance over frequency, not just DC ampacity and capacitor count | Eric Bogatin, *Signal and Power Integrity—Simplified*, 3rd ed., [Pearson](https://www.pearson.com/en-us/subject-catalog/p/signal-and-power-integrity-simplified/P200000000140/9780134513416); device/regulator data | Partly covered through rail budgets, DC-bias, ESR, and local loops. Target impedance, anti-resonance, regulator-loop interaction, and frequency-dependent capacitor/package/via models are gaps. | Add a PDN branch with `Ztarget = allowed rail disturbance / load step`, model validity, and measurement/simulation correlation. |
| High-frequency return current follows the nearby reference path; plane splits and shared impedance matter | [ADI mixed-signal grounding guidance](https://www.analog.com/en/resources/analog-dialogue/articles/what-are-the-basic-guidelines-for-layout-design-of-mixed-signal-pcbs.html); [ADI AN-1142](https://www.analog.com/en/resources/app-notes/an-1142.html); Henry Ott, *Electromagnetic Compatibility Engineering*, [Wiley](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470508510) | Agrees strongly. The preference for a continuous reference and planned returns is sound. | Ask “what is the complete current loop?” for every critical net and power stage; use a split only with device/system evidence and a defined crossing strategy. |
| Ground stitching vias are a return-path tool, not decoration | [TI high-speed interface layout guidance](https://www.ti.com/lit/an/spracp4/spracp4.pdf); [TI high-speed layout application brief](https://www.ti.com/document-viewer/lit/html/SLLA653) | Agrees. The local language avoids “via fence by habit.” | Require a reason and observable return path for each critical transition; verify proximity and symmetry against the relevant interface/device guide. |
| A USB-C receptacle used as a simple USB 2.0 sink/device needs the current Type-C pin, CC, VBUS, and role rules | [USB Type-C Release 2.5 page](https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25) | The local independent 5.1 kΩ Rd implementation and doubled D+/D− pin joins agree with the older cited spec. The clause references are to Release 2.0 and must be revalidated against Release 2.5. | Keep power role (Sink/Source) separate from data role (UFP/DFP); pin the current release and revalidate pin/table references. |
| USB 2.0 requirements remain applicable when USB-C is only the connector | [USB 2.0 specification package, 2025-06-03](https://www.usb.org/document-library/usb-20-specification); [USB-IF compliance program](https://usb.org/compliance) | Agrees. Local material correctly says Type-C wiring alone is not USB compliance. | Maintain separate gates for Type-C attach/power behavior, USB 2.0 electrical/protocol behavior, and product interoperability. |
| ATmega32U4 requires its device-specific USB passives, including 22 Ω series resistors and a 1 µF UCAP capacitor | [ATmega32U4 product/data sheet](https://www.microchip.com/en-us/product/atmega32u4) | Agrees. Do not turn these values into generic USB termination rules. | Bind each value to the device data-sheet section and tolerance; re-run if MCU/PHY changes. |
| Effective capacitance presented at VBUS and inrush must satisfy the applicable USB power rules | [USB 2.0 specification package](https://www.usb.org/document-library/usb-20-specification); [Microchip USB bus-power example](https://onlinedocs.microchip.com/oxy/GUID-C6020E95-38E0-47B1-9EF9-A035ACD4168B-en-US-1/GUID-A66FB49A-520B-4013-B6FB-3D52AD226BF8.html) | The 4.7 µF plus local decoupling budget is plausibly below 10 µF, but the skill must calculate **total effective** capacitance at the receptacle and test inrush/droop; nominal BOM sum is not compliance. | Record min/max/effective capacitance, bias/tolerance, all paths across VBUS, and measured attach behavior. |
| USB D+/D− is a nominal 90 Ω differential transmission-line environment; geometry comes from the production stack-up | [USB 2.0 specification package](https://www.usb.org/document-library/usb-20-specification); [Microchip AN1816](https://www.microchip.com/en-us/application-notes/an1816); [JLCPCB impedance calculator guide](https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator) | Agrees on target and stack-up dependence. The two-layer board correctly declines a controlled-impedance claim. | Never infer impedance from width/gap alone. Archive the fabricator stack-up and field-solver/calculator inputs; label uncontrolled prototypes explicitly. |
| Full-speed bit rate and short route length do not erase edge-rate, discontinuity, or return-path physics | Howard Johnson and Martin Graham, *High-Speed Digital Design*, [InformIT/Pearson](https://www.informit.com/store/high-speed-digital-design-a-handbook-of-black-magic-9780133957242); Bogatin, cited above | Local text is mostly careful but “short full-speed routing” can be misread as a general waiver. Its 4 mm skew limit is an internal criterion, not a USB compliance limit demonstrated by the cited sources. | Base transmission-line treatment on signal edge rate and interconnect delay; classify every numeric geometry/skew rule as normative, vendor-recommended, calculated, or project-derived. |
| Pair coupling, symmetry, minimal stubs/vias, continuous reference, and nearby return stitching improve USB routing | [Microchip AN1816](https://www.microchip.com/en-us/application-notes/an1816); [TI TM4C129x system design guidelines](https://www.ti.com/lit/an/spma056/spma056.pdf); [TI return-path guidance](https://www.ti.com/lit/an/spracp4/spracp4.pdf) | Agrees. However, recommendations from a hub or different MCU family are corroboration, not controlling ATmega limits. | Attach every borrowed numeric limit to the source device/interface; preserve only the physics-level pattern as reusable. |
| USB ESD suppressor capacitance, pinout, clamping, placement, and discharge return all matter | [ST USBLC6-2 data](https://www.st.com/en/protections-and-emi-filters/usblc6-2.html); [TI ESD and surge protection for USB](https://www.ti.com/lit/an/slvaf82b/slvaf82b.pdf) | Agrees on a low-capacitance array close to the connector and a short discharge path. | Add pin-map, dynamic-clamp/current-path, protected/unprotected coupling, CC/VBUS exposure, and exact layout review. |
| A component’s IEC 61000-4-2 rating does not prove the assembled product passes system ESD immunity | [IEC 61000-4-2:2025 scope](https://webstore.iec.ch/en/publication/68954); [ST USBLC6-2 product wording](https://www.st.com/en/protections-and-emi-filters/usblc6-2.html) | This limit is only implicit locally. The system has no executed ESD test. | Use “component-level test evidence” and “system immunity test” as separate fields; define enclosure, cable, contact/air points, levels, polarities, performance criteria, and test setup. |
| EMC is a product/system property involving emissions, immunity, cables, enclosure, current loops, and jurisdiction | [FCC Part 15 measurement guidance](https://apps.fcc.gov/oetcf/kdb/forms/FTSSearchResultPage.cfm?id=21079&switch=P); [IEC 61000-4-2:2025](https://webstore.iec.ch/en/publication/68954); Ott, cited above | Major gap. Local layout advice is good source control, but no product EMC target, pre-compliance plan, cable/common-mode analysis, or regulatory classification exists. | Add a requirements-first EMC branch and prohibit “EMC-ready/compliant” claims from schematic/layout inspection alone. |
| KiCad DRC checks only configured rules; router “optimal” values are not automatically min/max acceptance rules | [KiCad 10 PCB Editor](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html) | Agrees. This is one of the strongest local sections. | Pin KiCad and explicitly test min/max `diff_pair_gap`, uncoupled length, length/skew semantics, via count, parity, zones, and exclusions. |
| Zones must be current and inspected; connectivity does not prove an adequate high-frequency return | [KiCad 10 Getting Started](https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html); [KiCad 10 PCB Editor](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html) | Agrees. Local fresh-process refill and visible-copper inspection are good. | Pair machine connectivity with visual/geometry evidence; never use ratsnest or zero-open count as a return-path claim. |
| KLC is a library-contribution convention; the exact manufacturer drawing takes precedence | [KiCad Library Conventions](https://klc.kicad.org/) | Agrees in principle. The release evidence says footprints match pinned library geometry, which is weaker than showing every critical footprint matches its current manufacturer drawing. | Require manufacturer-drawing comparison for each critical/custom footprint; KLC conformance is a separate check. |
| Land patterns and assembly spacing depend on process, tolerances, inspection, test, and rework | [IPC-7351 scope/TOC](https://www.ipc.org/TOC/IPC-7351.pdf); [JLCPCB assembly terms](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service) | Agrees, but assembly acceptance class, stencil design, fiducials, cleanliness, and workmanship criteria are incomplete. | Make assembly process and acceptance criteria explicit; reconcile BOM/CPL/preview and exact MPN/footprint/polarity. |
| Supplier capability values are order-time inputs, not timeless design laws | [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities); [JLCPCB impedance guide](https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator) | Agrees. Current JLCPCB data still lists controlled impedance for 4 layers and above with ±10% tolerance, supporting the local no-claim stance for the two-layer order. | Store chosen service/options and access date; refresh before quote/order and when changing supplier. |
| Generated Gerber/drill and assembly files are the manufacturing contract and need independent inspection | [KiCad 10 GerbView](https://docs.kicad.org/10.0/en/gerbview/gerbview.html); [JLCPCB ordering instructions](https://jlcpcb.com/help/article/instructions-for-ordering) | Agrees strongly. The independent parsers and artifact hashes are good evidence. | Regenerate from a clean checkout, inspect all layers/drills/outline/mask/paste/legend, and reconcile release hashes. |
| Bare-board electrical test does not prove geometry, assembly, or function | [IPC-9252B scope/TOC](https://www.ipc.org/TOC/IPC-9252B.pdf) | Agrees exactly. | Keep fabrication electrical test, incoming inspection, assembly inspection, and functional test as separate gates. |
| USB enumeration is useful bring-up evidence, not USB certification | [USB-IF compliance program](https://usb.org/compliance); [USB 2.0 Electrical Compliance Test Specification v1.08](https://www.usb.org/document-library/usb-20-electrical-compliance-test-specification) | Agrees. Local claim language is appropriately conservative. | Reserve “USB compliant/certified” for the applicable program evidence; archive host/cable/orientation/interoperability results separately. |
| Bring-up should establish safe power, identity, clocks/reset, programming recovery, interfaces, and functional behavior with numerical limits | [Microchip 8-bit PIC/AVR design and troubleshooting checklist](https://onlinedocs.microchip.com/oxy/GUID-D6FD9F43-8DC4-476E-A55E-AA21FA1CC865-en-US-4/index.html); Hayes, Abrams, and Horowitz, *Learning the Art of Electronics*, 2nd ed., [Cambridge](https://www.cambridge.org/core/books/learning-the-art-of-electronics/9B9FA2FE6B1802BD4627B1F9825E8F0A) | Agrees. The local plan is concrete and correctly marked unexecuted. | Add expected resistance/current/rail windows, safe probing methods, fault-decision tree, instrument loading/bandwidth, uncertainty, and a signed as-run log. |

## Where the local material agrees with broader engineering teaching

### Circuit design

- Starting from exact part/package data, accounting for every power/reference/reset/programming pin, and recording each deviation from a reference design matches good professional practice.
- The separation between a component data sheet, a manufacturer reference design, and a community implementation is correct. A shipped board is evidence of one implementation, not a transferable proof.
- Worst-case ratings, startup states, fault paths, firmware/fuse dependencies, and recoverable programming access belong in the schematic review, not after layout.

### Grounding, return paths, and power integrity

- “Ground” is a current-return network, not an abstract zero-voltage label. Planning complete loops during placement is consistent with ADI guidance and the treatment in Bogatin, Johnson/Graham, and Ott.
- A continuous reference is usually safer than an arbitrary analog/digital split. Partition circuits and control shared impedance; split only when the system/device analysis supports it.
- Local decoupling is about loop inductance and transient current. The local emphasis on placement and connections is more useful than capacitor count alone.
- Power width must come from the actual current, copper, allowed rise/drop, ambient, length, and via transitions. The local refusal to universalize 15 mil is correct.

### USB 2.0 and Type-C

- The Type-C receptacle’s two CC pins need independent sink terminations for a passive sink; both plug orientations and A-to-C/C-to-C use must be tested.
- The ATmega’s 22 Ω data resistors and 1 µF UCAP capacitor are device requirements, while the connector’s Rd resistors are Type-C requirements. Keeping those categories distinct is correct.
- The pair should be short, symmetric, coupled where possible, minimally discontinuous, and continuously referenced. Protection belongs at the connector with a low-inductance discharge path.
- The two-layer geometry is correctly described as **not fabricator-controlled impedance**. This is honest engineering language.

### DFM, verification, and bring-up

- Exact order parameters and supplier capabilities are part of the design input. Designing away from absolute minima improves yield and flexibility.
- Inspecting generated Gerbers/drills and reconciling BOM/CPL/assembly preview is necessary; source CAD alone is not the manufacturing artifact.
- ERC, DRC, 3D, parser, connectivity, and firmware-build checks each prove limited propositions. The local “design checks passed, not hardware passed” language is exemplary.
- The staged bring-up plan, programming recovery, both connector orientations, matrix tests, reconnect/soak tests, and archived measurements are aligned with laboratory-oriented learning material.

## Contradictions, nuance, and corrections

### Internal inconsistencies found while creating the teaching fixture

The rows below describe the imported source state. The repository fixture now
uses 18 pF for C1/C2, Littelfuse `1206L025YR` with its 250 mA hold rating, and
the implemented QMK pin map; it also labels old Type-C clauses as historical.
The table is retained because detecting and resolving ledger drift is itself a
reusable review lesson.

| Issue | Evidence in local docs | Why it matters | Required correction |
|---|---|---|---|
| Crystal capacitors | `design-decisions.md` says two 22 pF; `engineering-calculations.md` calculates two 18 pF for a 12 pF-load crystal | BOM, schematic, calculation, and assembly instruction can silently diverge | Name the populated references/values in one authoritative design ledger; make CI compare schematic/BOM/calculation. |
| Fuse rating | `design-decisions.md` says a 500 mA resettable fuse; `engineering-calculations.md` says 250 mA PPTC hold rating | “500 mA” may be trip/current label rather than hold rating; temperature and voltage drop affect behavior | Record exact MPN plus hold/trip current at stated temperature, resistance, voltage rating, and the intended protection function. |
| Pin allocation | `research.md` proposes PB4/PB5/PB6/PB7/PE6 and PD4/PD6; `design-decisions.md` implements PB4/PB5/PB6/PC6/PD7 and PD0/PD1 | A portable agent may treat the older proposal as current | Mark proposed material superseded or generate all pin tables from one machine-readable contract. |
| Source revision | Several links use AN2519 revision A; a current official revision B is available | Clause/page references and recommendations can drift | Manifest revision B/current product source and archive the hash; retain old revision only as historical evidence. |
| Type-C clauses | Detailed pin/Rd citations are to Release 2.0; current USB-IF page is Release 2.5, published 2026-04-08 | Old facts may remain correct, but old clause numbers are not a current review | Revalidate against Release 2.5 and record the exact current sections/tables in the local evidence pack. |
| KiCad documentation | Source map frequently links `master`; the verified project used KiCad 10.0.5 | DRC features and length/skew semantics can change | Link version 10 documentation and pin CLI/container/plugin versions in a lock file. |
| Footprint evidence | Verification proves equality to pinned KiCad library geometry | Library equality does not alone prove equality to the exact component drawing | Add a drawing-to-footprint evidence record for J1, U1, protection device, crystal, diode, and other critical packages. |
| VBUS capacitance | `research.md` records the ATmega recommendation for 10 µF; the release calculation intentionally uses 4.7 µF plus local decoupling | A recommendation may be traded off against inrush, but the deviation must be deliberate and tested | Put the deviation, total effective-capacitance bounds, inrush/droop test, and acceptance limit in the canonical design ledger. |
| USB geometry gate | The source-map U1 gate asks for a pair-geometry calculation; the project records a non-controlled-impedance two-layer exception | “Not controlled” does not remove the need to estimate and document risk | Attach the estimate and inputs, while keeping the manufacturing claim explicitly uncontrolled. |
| Bring-up limits | T1 asks for numerical limits, while the as-yet unexecuted plan includes “no low-ohmic short,” “stable,” “plausibly,” and “no heating” | Different operators can reach different pass/fail decisions | Replace qualitative terms with thresholds or a bounded engineering decision tree before execution. |

### Scope and terminology corrections

- **Do not say hierarchy conflicts always resolve “upward.”** A current fabricator capability cannot override USB electrical requirements, and USB-IF does not define an assembler’s paste process. Resolve by owning authority and scope.
- **Separate requirement, recommendation, calculation, and project decision.** “90 Ω differential” is an interface target; “three-to-five times spacing” is device/application guidance; 0.20/0.20 mm is this board’s geometry; 4 mm skew is an internally encoded limit unless a controlling source is documented.
- **Separate Type-C roles.** Sink/Source describes power; UFP/DFP describes USB data. This macro pad is both Sink and UFP, but a reusable skill must not treat the pairs as synonyms.
- **Do not infer bandwidth from bit rate alone.** USB full-speed is 12 Mb/s, yet edge rate and interconnect delay govern transmission-line behavior. The short route may have ample prototype margin, but it does not null the 90 Ω environment.
- **Do not equate a ground pour with a reference plane.** A two-layer pour may be cut by routes, pads, clearances, and narrow necks. Visual return-path evidence is still required.
- **Do not equate device-level ESD data with system immunity.** ST explicitly describes its IEC evidence at device level; IEC 61000-4-2 is an equipment/system test method.
- **Do not equate assembler DFM review with functional test.** JLCPCB’s own assembly terms state that it does not power-test every board and automated part matching requires customer confirmation.
- **Do not use “verified” without a noun.** Prefer “ERC-verified,” “DRC-checked against rule set X,” “Gerber parsed,” “prototype functionally tested,” or “USB-IF certified.”
- **Treat legacy IPC documents accurately.** IPC's [revision table](https://www.ipc.org/ipc-document-revision-table) marks IPC-2152, IPC-7351B, and IPC-9252B as no longer maintained. They remain useful scoped baselines, not evidence that a design uses the current maintained requirement set; select current applicable design, performance, process, and acceptability documents for the product contract.

## Gaps relative to other circuit classes and textbooks

The present material should become the `low-voltage-mcu-usb2` branch of a larger curriculum, not the root curriculum itself.

| Circuit class | What transfers from the macro-pad work | Additional curriculum required |
|---|---|---|
| Linear/precision analog and data conversion | Exact part data, pin ledgers, local loops, continuous reference, test points | Noise/error budget, source impedance, bias/leakage, guard/Kelvin routing, reference stability, ADC drive/settling, alias filtering, thermal EMF, calibration |
| Switching regulators and power converters | Rail budget, decoupling, current/voltage-drop analysis, fault paths | Hot-loop derivation by switching state, compensation/stability, switch-node containment, magnetics, snubbers, thermal loss, surge/load dump, safe operating area, conducted/radiated EMI; see [ADI AN-139](https://www.analog.com/en/resources/app-notes/an-139.html) |
| Motors, solenoids, relays, and high current | Width/via budgeting and bring-up current limiting | Inductive energy, recirculation, current sense, gate drive, dead time, isolation, creepage, connector heating, fault containment, mechanical/EMC environment |
| RF and antennas | Stack-up control, short paths, reference continuity, generated-output review | RF launch/connector models, matching networks, antenna keepouts, enclosure/user detuning, material Dk/loss at frequency, VNA calibration/de-embedding, regulatory radio requirements |
| Isolation, mains, hazardous voltage | Evidence packs, package drawings, DFM | Hazard analysis, applicable safety standard, insulation system, working voltage/transients/pollution/material group, creepage/clearance, slots/barriers, hipot, fuse/earthing, certified components. Low-voltage IPC clearances are not substitutes. |
| Dense BGA/HDI/high-speed serial | Pin maps, custom rules, impedance stack-up, return vias | Escape/via technology, reference transitions, insertion/return loss, crosstalk, fiber weave, glass/resin Dk, backdrill, coupons/TDR, microvia reliability, X-ray/AXI |
| Production/high-reliability electronics | Release manifests and separate test gates | IPC class/acceptance criteria, traceability, process capability, cleanliness, environmental qualification, derating, lifecycle/obsolescence, change control, failure analysis |

Textbook comparison:

- Bogatin’s model-driven SI/PI treatment exposes the main local gap: checks should derive from edge rate, impedance, current spectrum, and allowed noise, not primarily from geometric heuristics.
- Johnson and Graham reinforce that apparently “digital” interconnects are analog transmission structures. This supports the local return-path emphasis but argues against using route length and bit rate as the whole USB rationale.
- Ott’s equipment-level EMC treatment adds cables, enclosure, common-mode conversion, grounding, shielding, filtering, emissions, immunity, and pre-compliance. The local corpus currently concentrates on PCB source control and ESD parts.
- Coombs and Holden’s *Printed Circuits Handbook* covers the broader supply chain, fabrication, process control, bare-board/assembly test, quality, and reliability that are only partly represented in the local JLCPCB release workflow: [publisher page](https://www.mheducation.com/highered/mhp/product/printed-circuits-handbook-seventh-edition.html).
- Horowitz and Hill’s *The Art of Electronics*, 3rd ed., and Hayes/Abrams/Horowitz’s hands-on lab course are useful for circuit behavior and bench judgment, but exact production designs still defer to current component and interface sources: [Cambridge listing](https://www.cambridge.org/gb/search?query=art+of+electronics).

## Recommended skill rewrite

Use a thin router plus disclosed domain skills. Stable procedure belongs in skills; volatile facts belong in manifests and project evidence.

### 1. `pcb-evidence-router`

Trigger: any schematic, PCB, fabrication, review, or release task.  
Steps:

1. Classify voltage/energy, interfaces, frequencies/edge rates, analog sensitivity, power conversion, RF, isolation, environment, jurisdiction, assembly volume, and claim level.
2. Select the required domain skills and source classes.
3. Create a gate matrix with an owner, evidence artifact, and blocking criterion for every applicable domain.

Completion: every requirement has a controlling source or is explicitly unresolved; every unresolved controlling item blocks the appropriate gate.

### 2. `circuit-evidence-design`

Trigger: selecting parts, drawing/reviewing a schematic, or changing a functional block.  
Core behaviors:

- Exact MPN/package and pin ledger; datasheet, errata, package, lifecycle, and reference implementation.
- Per-block requirement → implementation → calculation → verification traceability.
- Worst-case/tolerance/derating, startup/reset/strap/unused-pin states, protection/fault/back-power paths, firmware/fuse dependencies, test/programming access.
- ERC plus manual functional checks; explicit list of facts ERC cannot prove.

Completion: all non-trivial blocks have evidence records and every symbol pin/footprint pad/firmware pin maps to the same machine-readable source of truth.

### 3. `pcb-return-pdn-layout`

Trigger: placement, stack-up, power routing, grounding, decoupling, or any fast-edge interface.  
Core behaviors:

- Draw complete signal and power current loops before routing.
- Derive stack-up, impedance, trace/via capacity, voltage drop, target impedance, decoupling topology, and return transitions from named inputs.
- Distinguish DC, low-frequency, and high-frequency return behavior.
- Use continuous references by default; any split requires an explicit circuit model and crossing plan.
- Route critical nets only after constraints are encoded and testable.

Completion: calculations and rules agree; every critical route has visible reference continuity and all non-automatable checks have archived evidence.

### 4. `usb2-typec-device`

Trigger: USB 2.0 through a USB-C receptacle or captive cable.  
Branches: FS/LS versus HS; Sink/UFP versus other roles; bus-powered versus self-powered; passive Rd versus controller/PD.  
Core behaviors:

- Pin the current USB 2.0 and Type-C releases, the exact PHY/controller data, connector drawing, ESD/protection data, and compliance target.
- Audit A/B D+/D− joins, independent CC behavior, VBUS/GND contacts, SBU/unused pins, shell/chassis, back-power, inrush/effective capacitance, descriptor/power policy, and both orientations/cable classes.
- Derive impedance geometry from production stack-up; record coupled/uncoupled length, discontinuities, skew, vias, return reference, protection path, and probe/test method.

Completion: electrical and power claims are tied to the applicable spec/device clauses; enumeration evidence is never labeled compliance evidence.

### 5. `pcb-emc-esd`

Trigger: external connectors, cables, switching power, motors, clocks, enclosure, product release, or an EMC/immunity claim.  
Core behaviors:

- Define jurisdiction/product standard, emissions class, immunity tests/levels/performance criteria, cable and enclosure configuration.
- Identify differential- and common-mode current paths, apertures, cable coupling, high-dv/dt and high-di/dt loops, shield/chassis strategy, filtering and protection placement.
- Separate component qualification, design review, pre-compliance measurement, and accredited/compliance test.

Completion: there is an executable test matrix and no system claim rests on a component data sheet or visual inspection alone.

### 6. `pcb-dfm-assembly-release`

Trigger: footprint creation, supplier selection, fab/assembly outputs, or release.  
Core behaviors:

- Pin supplier/order capability, stack-up, material/copper/finish, drills/vias, mask/paste, edge/cutout, impedance, panel and assembly process.
- Validate critical footprints against manufacturer drawings and assembly process; then check KLC/IPC convention as applicable.
- Reconcile BOM/CPL/preview/designators/side/rotation/polarity; define workmanship/inspection/test acceptance.
- Generate from clean checkout; inspect Gerbers/drills/netlist/assembly outputs independently; hash the release.

Completion: the exact order configuration is reproducible, artifacts agree, and supplier DFM questions are resolved without silently changing design intent.

### 7. `pcb-verification-bringup`

Trigger: release claims, first article, failure diagnosis, or production test.  
Core behaviors:

- Use a claim-evidence vocabulary: source parse, ERC, DRC, parity, geometry, manufacturing-output, bare-board test, assembly inspection, functional test, environmental/compliance test.
- Create safe first-power limits, expected rails/current/resistance, probing plan, programming recovery, clock/reset/strap checks, interface and functional tests, soak/fault tests, and serial-numbered logs.
- Record instrument model/calibration, setup, loading/bandwidth, uncertainty, raw data, failures, and corrective actions.

Completion: every stated claim names the evidence level and design/firmware/artifact hashes; unexecuted tests remain visibly pending.

## TDD policy for agent skills and PCB checks

Each deterministic check needs a fixture that proves both detection and non-regression.

1. **Red:** add or select a minimal KiCad fixture containing one known defect, such as swapped symbol/footprint pads, missing power pin, wrong CC topology, stale zone, unconfigured differential gap, open ground island, BOM/CPL mismatch, or conflicting populated value.
2. Assert that the authoritative/native tool detects the defect when it supports the claim. If it cannot, assert that the supplemental check reports its limited scope and never impersonates native ERC/DRC.
3. **Green:** correct only the defect and show the expected report change.
4. **Refactor:** extract reusable parsing/rules without weakening the failing fixture.
5. Run the complete fixture matrix in a pinned clean environment; archive machine-readable reports and human-review artifacts.

Minimum test matrix:

- KiCad versions explicitly supported by the toolkit.
- Valid board, one-fault boards, and ambiguous/unsupported constructs.
- Windows/macOS/Linux path and line-ending behavior where scripts are portable.
- Source/schema drift tests for KiCad file versions and CLI output.
- Golden manifest/hash tests for release artifacts.
- Claim tests: ensure reports say “not checked/unknown” when evidence is unavailable instead of manufacturing a pass.

Do not automate physics by majority vote over reference boards. Automated checks should verify a sourced project rule, calculate a documented model, or flag missing evidence.

## Portable repository and corpus design

Suggested public repository layout:

```text
README.md
LICENSES/
NOTICE.md
AGENTS.md
skills/
  pcb-evidence-router/SKILL.md
  circuit-evidence-design/SKILL.md
  pcb-return-pdn-layout/SKILL.md
  usb2-typec-device/SKILL.md
  pcb-emc-esd/SKILL.md
  pcb-dfm-assembly-release/SKILL.md
  pcb-verification-bringup/SKILL.md
curriculum/
  fundamentals.md
  source-hierarchy.md
  claim-language.md
references/
  manifest.yaml
  README.md
schemas/
fixtures/
  valid/
  invalid-one-fault/
scripts/
tests/
examples/
  tenkey-macropad/
```

`references/manifest.yaml` should contain, per item:

- stable ID, title, publisher/owner, document/revision/date, source tier and claim domain;
- canonical URL, retrieval date, SHA-256, media type, and local filename if redistribution is allowed;
- license identifier or `LicenseRef-Proprietary-Link-Only`, attribution, modification status, and redistribution decision;
- clause/page pointers used by local claims, supersedes/superseded-by, and review-expiry trigger;
- applicability: exact device/package/board revision/interface role/stack-up/fabricator/KiCad version;
- status: current, historical, superseded, unavailable, or requires licensed access.

## Licensing and redistribution policy

This is a conservative operational policy, not legal advice.

1. **Original toolkit code and skills:** choose an explicit permissive code license such as Apache-2.0 or MIT. If long-form curriculum text should remain share-alike, dual-license docs separately and mark every file with SPDX identifiers.
2. **USB-IF specifications:** keep link, revision, hash, and clause metadata. The current [Type-C Release 2.5 page](https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25) states a limited-purpose copyright license; do not commit the ZIP/PDF to a public repository without a reviewed permission basis.
3. **IPC, IEC, ANSI, and paid standards:** commit bibliographic metadata, public scope/TOC links, and original summaries only. Users obtain licensed copies separately. Never copy normative tables or substantial text into skills.
4. **Textbooks:** commit citations, ISBN/DOI, reading map, and original conclusions. Do not commit scans, chapters, answer keys, or lengthy excerpts.
5. **Vendor data sheets/application notes/CAD:** default to link-only unless the publisher provides clear redistribution terms. A public download URL is not itself a redistribution license. Store hashes so another machine can verify a separately downloaded copy.
6. **KiCad libraries:** official libraries are [CC BY-SA 4.0 with a stated design-output exception](https://gitlab.com/kicad/libraries/kicad-footprints/-/blob/master/LICENSE.md). Using library items in a design does not by itself force the design to be share-alike, but redistributing a library collection requires the applicable license and attribution. Preserve license files and source revision.
7. **Open hardware reference designs:** include files only under their actual hardware/documentation/software licenses and preserve notices. OSHWA certification/definition is not a substitute for a license; see [OSHWA sharing best practices](https://oshwa.org/resources/sharing-best-practices/).
8. **Manufacturer and distributor part data:** avoid scraped catalogs. Prefer MPN plus manufacturer source, and treat distributor inventory/pricing as volatile metadata refreshed at use time.
9. **Local caches:** place downloaded restricted sources in a gitignored cache populated by a script after the user accepts the source terms. The script should verify SHA-256 and fail closed on a mismatch.
10. **Secrets and machine portability:** no API tokens, cookies, account IDs, quotes, addresses, or credentials. Use `.env.example` with names only, OS keychain/environment injection, relative repository paths, and documented tool-version bootstrap.

Recommended repository controls:

- `NOTICE.md` lists third-party materials and attribution.
- `LICENSES/` carries the exact license texts required for redistributed content.
- CI rejects unknown-license binary additions under `references/`.
- CI scans for secrets and absolute home-directory paths.
- A source-refresh job reports changed hashes/revisions but does not silently update engineering claims.
- Reproducibility tests run without network access from a clean checkout; optional source download is a separate step.

## Curriculum sequence

1. **Electrical foundations and laboratory practice:** Ohm/Kirchhoff, real R/L/C behavior, time/frequency domain, safe measurement and instrument loading. Use *The Art of Electronics* and *Learning the Art of Electronics* as guided learning, not copyable corpus.
2. **Evidence-driven circuit design:** requirements, data sheets/errata, exact parts/packages, worst-case calculations, power/reset/clock/programming, fault paths.
3. **PCB interconnect physics:** edge rate, transmission lines, current loops, impedance, crosstalk, return discontinuities. Use Johnson/Graham and Bogatin.
4. **Power integrity:** rail budgets, target impedance, decoupling hierarchy, regulator/load interaction, DC drop/current/thermal limits.
5. **Grounding and EMC:** common impedance, differential/common mode, stack-up, cables/enclosure, ESD/EFT/surge as applicable, pre-compliance. Use Ott and the applicable product standards.
6. **KiCad execution:** version-pinned schematic/PCB workflows, custom rules, zones, library validation, CLI, generated outputs, and tool limits.
7. **Domain labs:** USB 2.0 Type-C device first; then precision analog, switch-mode power/motor, RF, and isolation/high-voltage as separate branches.
8. **DFM/assembly/test:** supplier contract, IPC concepts, footprint/process tolerances, stencil/panel/inspection, output review, bare-board and functional test.
9. **TDD release project:** intentionally flawed fixtures, corrected design, clean build, independent output inspection, first-article bring-up, failure report, and bounded claims.

## Direct source list

### Normative, regulatory, and official product sources

- USB-IF, [USB 2.0 specification package, 2025-06-03](https://www.usb.org/document-library/usb-20-specification).
- USB-IF, [USB Type-C Cable and Connector Specification Release 2.5, 2026-04-08](https://www.usb.org/document-library/usb-type-cr-cable-and-connector-specification-release-25).
- USB-IF, [USB 2.0 Electrical Compliance Test Specification v1.08, 2026-04-21](https://www.usb.org/document-library/usb-20-electrical-compliance-test-specification).
- USB-IF, [Compliance Program](https://usb.org/compliance) and [compliance checklists](https://www.usb.org/checklists).
- Microchip, [ATmega32U4 product page and current data sheet](https://www.microchip.com/en-us/product/atmega32u4).
- Microchip, [AN2519 AVR Microcontroller Hardware Design Considerations, revision B](https://www.microchip.com/content/dam/mchp/documents/MCU08/ApplicationNotes/ApplicationNotes/AN2519-AVR-Microcontroller-Hardware-Design-Considerations-00002519B.pdf).
- STMicroelectronics, [USBLC6-2 product page/data/CAD](https://www.st.com/en/protections-and-emi-filters/usblc6-2.html).
- GCT, [USB4085 drawing](https://gct.co/files/drawings/usb4085.pdf).
- IEC, [IEC 61000-4-2:2025 scope](https://webstore.iec.ch/en/publication/68954).
- FCC, [Part 15 measurement-procedure guidance](https://apps.fcc.gov/oetcf/kdb/forms/FTSSearchResultPage.cfm?id=21079&switch=P).

### Official implementation and tool sources

- Microchip, [AN1816 USB224x/225x PCB Design Guidelines](https://www.microchip.com/en-us/application-notes/an1816).
- Microchip, [8-bit PIC/AVR Design and Troubleshooting Checklist](https://onlinedocs.microchip.com/oxy/GUID-D6FD9F43-8DC4-476E-A55E-AA21FA1CC865-en-US-4/index.html).
- TI, [TM4C129x System Design Guidelines](https://www.ti.com/lit/an/spma056/spma056.pdf).
- TI, [High-Speed Interface Layout Guidelines](https://www.ti.com/lit/an/spracp4/spracp4.pdf).
- TI, [ESD and Surge Protection for USB Interfaces](https://www.ti.com/lit/an/slvaf82b/slvaf82b.pdf).
- Analog Devices, [AN-1142 high-speed ADC PCB layout](https://www.analog.com/en/resources/app-notes/an-1142.html).
- Analog Devices, [Mixed-Signal PCB Layout Guidelines](https://www.analog.com/en/resources/analog-dialogue/articles/what-are-the-basic-guidelines-for-layout-design-of-mixed-signal-pcbs.html).
- Analog Devices, [AN-139 Power Supply Layout and EMI](https://www.analog.com/en/resources/app-notes/an-139.html).
- KiCad, [version 10 PCB Editor](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html), [Schematic Editor](https://docs.kicad.org/10.0/en/eeschema/eeschema.html), [GerbView](https://docs.kicad.org/10.0/en/gerbview/gerbview.html), and [CLI](https://docs.kicad.org/10.0/en/cli/cli.html).
- KiCad, [Library Conventions](https://klc.kicad.org/) and [library license](https://gitlab.com/kicad/libraries/kicad-footprints/-/blob/master/LICENSE.md).
- IPC, [design standards index](https://www.ipc.org/ipc-design-standards), [IPC-2152 scope](https://www.ipc.org/TOC/IPC-2152.pdf), [IPC-7351 scope](https://www.ipc.org/TOC/IPC-7351.pdf), and [IPC-9252B scope](https://www.ipc.org/TOC/IPC-9252B.pdf).
- JLCPCB, [capabilities](https://jlcpcb.com/capabilities/pcb-capabilities), [impedance calculator guide](https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator), [BOM/CPL preparation](https://jlcpcb.com/help/article/advice-for-bom-and-cpl-files-preparation), [assembly terms](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service), and [ordering instructions](https://jlcpcb.com/help/article/instructions-for-ordering).

### Authoritative books and learning material

- Eric Bogatin, *Signal and Power Integrity—Simplified*, 3rd ed., Pearson, 2018/2021 catalog records, ISBN 978-0-13-451341-6: [publisher page](https://www.pearson.com/en-us/subject-catalog/p/signal-and-power-integrity-simplified/P200000000140/9780134513416).
- Howard W. Johnson and Martin Graham, *High-Speed Digital Design: A Handbook of Black Magic*, Prentice Hall/Pearson, 1993, ISBN 978-0-13-395724-2: [InformIT/Pearson publisher page](https://www.informit.com/store/high-speed-digital-design-a-handbook-of-black-magic-9780133957242).
- Henry W. Ott, *Electromagnetic Compatibility Engineering*, Wiley, 2009, ISBN 978-0-470-18930-6, DOI 10.1002/9780470508510: [publisher page](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470508510).
- Clyde F. Coombs Jr. and Happy T. Holden, eds., *Printed Circuits Handbook*, 7th ed., McGraw Hill, 2016, ISBN 978-0-07-183395-0: [publisher page](https://www.mheducation.com/highered/mhp/product/printed-circuits-handbook-seventh-edition.html).
- Paul Horowitz and Winfield Hill, *The Art of Electronics*, 3rd ed., Cambridge University Press, 2015: [publisher listing](https://www.cambridge.org/gb/search?query=art+of+electronics).
- Thomas C. Hayes, David Abrams, and Paul Horowitz, *Learning the Art of Electronics: A Hands-On Lab Course*, 2nd ed., Cambridge University Press, 2025, ISBN 978-1-009-53518-2, DOI 10.1017/9781009535199: [publisher page](https://www.cambridge.org/core/books/learning-the-art-of-electronics/9B9FA2FE6B1802BD4627B1F9825E8F0A).

## Bottom line

The local work should be preserved as a high-quality case study and fixture, after its ledgers are reconciled. The reusable learning is the **evidence process**—claim scoping, exact-source traceability, machine-checkable rules, bounded verification, and staged physical test—not any one trace width, gap, capacitor value, via pattern, or supplier capability. A portable repository should encode that process in small domain skills, test it against known-good and one-fault KiCad fixtures, and keep copyrighted or volatile source material in a licensed, hashed, link-first manifest.
