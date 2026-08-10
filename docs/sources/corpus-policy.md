# Reference corpus and licensing policy

Store evidence metadata before storing files. Each record must name the exact
device or board revision, immutable source revision where possible, document
revision, retrieval date, license, redistribution status, validation claims,
known errata, and the design pattern extracted from it.

Assign authority by scope: standards/law own compliance; exact-part documents own
the component; the quoted fabricator/assembler process owns producibility;
version-matched KiCad documentation owns tool behavior; each IPC document owns
its named design/fabrication/assembly/acceptance scope. Application notes and
official evaluation boards guide implementation. Textbooks explain physics and
judgment; community/open-hardware boards provide comparative examples.

Resolve conflicts within their applicable scope and record the decision. Reference designs provide
implementation evidence, never proof by popularity. Revalidate a copied circuit
against the exact component, package, voltage, clock, stackup, and production
process in the new design.

Commit third-party files only when their license permits redistribution and the
license/attribution travels with the file. Otherwise commit a link, bibliographic
record, hash, and extraction notes. Never copy full textbooks, paywalled
standards, proprietary Gerbers, or vendor assets with unclear terms.

Keep reference cohorts distinct: two-layer versus impedance-controlled
multilayer, full-speed versus high-speed USB, prototype versus production,
official evaluation boards versus community boards, and claimed validation
versus independently observed results.
