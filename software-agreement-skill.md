---
name: software-agreement-bundle
description: Review a software project repository and generate a Software Development Agreement (legal contract between a freelance contractor and a client) plus a Project Specification, written as if the project being reviewed is what will be commissioned. Use when Copilot needs to produce client-ready contract and spec documents from an existing codebase.
---

# Software Agreement Bundle

Use this skill to reverse-engineer a software project into the contractual and specification documents that would have been used to commission it. The output should read like work produced by a senior freelance engineer and a commercial lawyer collaborating on a client engagement: precise scope, practical milestones, explicit IP and payment terms, and acceptance criteria grounded in what the software actually does.

## Core Philosophy

Produce two documents, nothing more:

1. `docs/software-development-agreement.md` — A master Software Development Agreement with an embedded Statement of Work, covering legal terms, deliverables, milestones, payment, IP ownership, and acceptance.
2. `docs/project-spec.md` — A technical Project Specification covering system purpose, architecture, module inventory, data models, API surfaces, third-party dependencies, and out-of-scope items.

Convert both to DOCX:

1. `docs/software-development-agreement.docx`
2. `docs/project-spec.docx`

Keep all Markdown and DOCX files in `docs`. Do not create additional report files or subdirectories unless explicitly asked.

## Repository Review

Before writing either document, inspect the actual project. Evidence sources include:

- Package metadata (`pyproject.toml`, `package.json`, `pom.xml`, `Cargo.toml`, etc.)
- Source tree structure and module boundaries
- README, existing docs, usage guides
- Route definitions, API handlers, schemas, models
- Test files and CI configuration
- Configuration files and environment variable patterns
- Migration scripts, seed data, Dockerfile or Compose files
- Any existing specification, design notes, or architecture diagrams

Identify concretely:

- What the software does and who it is for
- The primary technical components and their boundaries
- The public API or user-facing interface surface
- Data persistence approach and schema
- Third-party integrations (payment providers, auth services, cloud APIs, etc.)
- Testing strategy and automation present in the repository
- Deployment and runtime environment assumptions
- Obvious features that are explicitly absent or incomplete

Do not invent scope. If a feature is not evidenced by the repository, either exclude it or flag it as absent.

## Document 1 — Software Development Agreement

The `Document Type` field becomes the cover-page subtitle in the DOCX output. Use `Software Development Agreement and Statement of Work` verbatim.

### Agreement Structure

Number every section. Write each section as a professional legal clause — short, unambiguous paragraphs. Use plain English. Avoid archaic legalese, but preserve standard commercial contract precision.

Include these sections in order:

1. **Agreement Overview** — Brief statement of purpose. Identify that the document includes a master agreement and a Statement of Work.
2. **Parties** — Named placeholders for Client and Contractor legal names and addresses. Use `[Client Legal Name]`, `[Client Address]`, `[Contractor Legal Name]`, `[Contractor Address]` as fill-in tokens.
3. **Project Background** — Two to four sentences describing what the software does and why the client is commissioning it, derived from the repository.
4. **Services** — What Contractor will provide. Reference the Statement of Work.
5. **Independent Contractor Status** — Standard clause: not an employee; responsible for own taxes, tools, staffing, and methods.
6. **Project Management and Communication** — Points of contact, update cadence, Client obligations for access and review feedback.
7. **Deliverables** — Table of concrete deliverables with a one-sentence description each. Derive these from what is actually present in the repository: source code modules, tests, documentation, Docker or deployment artifacts.
8. **Payment Terms** — Two subsections:
   - Fixed-price milestone table keyed to the SOW milestones, with `[Amount]` tokens.
   - Time-and-materials alternative with `[Hourly Rate]` and `[Invoice Cadence]` tokens.
9. **Change Orders** — Clause requiring written approval for scope changes. List four to eight concrete change-order examples derived from what is visibly absent from the repository.
10. **Acceptance Testing** — Review period with `[Number]` token, deemed-accepted fallback, defect notice requirement.
11. **Intellectual Property Ownership** — Assignment to Client on full payment, Contractor retention of pre-existing tools and methods, license grant for incorporated pre-existing materials, third-party license pass-through. Include a plain-English note that owner should have counsel review IP assignment language.
12. **Confidentiality** — Mutual obligation, permitted use limited to performing the agreement, reasonable protection standard, standard carve-outs (public domain, independent development, third-party receipt, legal compulsion).
13. **Security and Credentials** — Client owns production accounts and credentials; payment card data must be handled through approved payment providers only.
14. **Warranties and Disclaimers** — Professional and workmanlike warranty; disclaimer of error-free or uninterrupted operation; Client responsibility for business, legal, and compliance decisions.
15. **Limitation of Liability** — Mutual cap at fees paid during `[Number]` preceding months; mutual exclusion of consequential damages; carve-outs for confidentiality breach, IP infringement, fraud, and willful misconduct.
16. **Termination** — Material breach termination after `[Number]`-day cure period; Client termination for convenience with `[Number]`-day notice; payment for accepted work on termination.
17. **Governing Law and Dispute Resolution** — `[State/Country]` governing law, good-faith negotiation before litigation, injunctive relief exception.
18. **Entire Agreement** — Supersedes prior proposals, emails, and estimates.

Separate the Statement of Work from the master agreement with a `<!-- pagebreak -->` comment.

### Statement of Work Structure

Continue section numbering from the master agreement:

19. **SOW Summary** — Two to three sentences summarising what Contractor will build, naming the primary technology choices evidenced in the repository.
20. **Technical Scope** — Numbered subsections per major system component. Each subsection lists the specific implementation responsibilities as a bullet list. Use only items evidenced by the repository; do not pad scope with features that are not present.
21. **Out of Scope** — Bullet list of items explicitly excluded. Derive these from what is absent or mentioned but not implemented. Always include: attorney-reviewed legal terms, production hosting account setup, production monitoring and incident response, and any platform-specific certifications.
22. **Milestones and Timeline** — Table with milestone name, deliverables summary, and `[Duration]` token. Use five milestones as a default: Discovery, Backend Foundation, Frontend/Core Feature Layer, Integrations (payments, auth, third-party), Testing and Handoff.
23. **SOW Acceptance Criteria** — Bullet list of concrete, testable conditions for project acceptance. Each criterion should be verifiable without subjective judgment: tests pass, build succeeds, pages load, integrations return expected responses.

## Document 2 — Project Specification

### Cover Block

```md
# Project Specification

**Project:** [Project Name from repository]
**Document Type:** Technical Project Specification
**Version:** 1.0
**Date:** [Today's date]
**Status:** Draft for Owner Review
```

### Spec Structure

Use the following sections. Write in a direct technical voice — this document is for engineers and technical reviewers, not clients.

1. **Purpose and Goals** — What the software does and who uses it. One short paragraph.
2. **System Overview** — Architecture pattern (e.g., REST API + SPA, monolith, microservices). Primary language(s) and frameworks. Runtime and deployment model.
3. **Module Inventory** — Table of source modules/packages with a one-line description of each. Derive entirely from the repository structure.
4. **Data Model** — Key entities, their primary fields, and relationships. Use a table or structured list. Note the persistence technology (SQLite, Postgres, MongoDB, etc.).
5. **API Surface** — Table or grouped list of primary routes, HTTP method, a one-line description. Include only routes evidenced in the repository.
6. **Third-Party Dependencies** — Table of external services and packages that are non-trivial dependencies: payment providers, auth services, cloud SDKs, notable open-source libraries. Note the purpose of each.
7. **Testing Strategy** — What is tested, what framework is used, and test coverage approach. Note any CI configuration present.
8. **Configuration and Environment** — Key environment variables or configuration files. Note which are required for runtime and which are optional.
9. **Deployment** — Docker/Compose or other deployment artifacts present. Known deployment assumptions.
10. **Known Limitations and Gaps** — Features that are absent or incomplete based on repository evidence. Be candid.
11. **Recommended Next Steps** — Three to six prioritized improvements or additions that are clearly warranted by the current state of the project.

## Formatting Rules

Both documents should use clean, conversion-friendly Markdown that the `mdx` CLI handles correctly:

- One `#` H1 title per document (the cover block title).
- `##` H2 for numbered top-level sections.
- `###` H3 for subsections within a section.
- Prose paragraphs for clause text.
- Bullet lists for enumerated items without numeric ordering requirements.
- Tables for deliverables, milestones, API routes, and dependency inventories.
- `<!-- pagebreak -->` between the master agreement and Statement of Work in the agreement document.
- Fill-in tokens use `[Square Bracket]` notation so they are visually distinct in the DOCX output.
- Do not use Mermaid diagrams — the converter renders them as code blocks.

## Conversion

```bash
mdx convert docs/software-development-agreement.md --style professional
mdx convert docs/project-spec.md --style professional
```

Or convert the whole docs directory at once:

```bash
mdx convert docs/ --style professional --force
```

## Avoid

- Invented features not evidenced by the repository.
- Vague scope language like "and other features as needed" without a change-order clause.
- Personal emails or private identifiers in fill-in tokens.
- Mermaid diagrams.
- Excessive tables — use prose for clauses, tables only for deliverables, milestones, and inventories.
- Repeating the same content in both documents — the agreement covers legal and commercial terms; the spec covers technical detail.

## Final Response

Return a concise summary with:

- Files created (`docs/software-development-agreement.md`, `docs/project-spec.md`).
- DOCX files generated.
- Key scope items identified from the repository.
- Fill-in tokens that the owner must complete before use.
- A reminder that the agreement is a template and requires legal review before signing.
