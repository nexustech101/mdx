---
name: software-documentation-bundle
description: Generate professional engineering reports for a software project and convert them with the mdx CLI. Use when Copilot needs to inspect a repository, produce senior-engineer-quality Markdown documentation, keep Markdown and DOCX files together in docs, and avoid boilerplate-heavy or table-heavy report packs.
---

# Software Documentation Bundle

Use this skill to create professional engineering documentation for a software project. The output should read like work from a senior freelance engineer preparing a client-facing technical report: direct, evidence-based, candid about uncertainty, and useful for decision-making.

## Core Philosophy

Prefer fewer, better documents. Do not create a five-document template pack unless the user explicitly asks for it.

Default to:

1) `docs/engineering-report.md`
2) `docs/architecture.md`
3) `docs/project-spec.md`
4) `docs/api-reference.md`

Then convert them to:

1. `docs/engineering-report.docx`
2. `docs/architecture.docx`
3. `docs/project-spec.docx`
4. `docs/api-reference.docx`

Keep all Markdown and DOCX deliverables in `docs`. Do not create a separate `dist/docx` tree unless the user explicitly requests that layout.

## Repository Review

Before writing, inspect the actual project. Use source files, package metadata, README/usage docs, command definitions, tests, configuration, and existing documentation as evidence.

Identify:

- What the project does.
- Who the project is for.
- The public interfaces and workflows.
- The actual architecture and module boundaries.
- Operational assumptions and dependencies.
- Known limitations and risks.
- Obvious next engineering improvements.

Do not invent implementation details. If a feature is not visible in the repository, say so plainly.

## Writing Standard

Write in a professional engineering voice. The report should have judgment and prioritization, not just inventory.

Use narrative sections for analysis. Use bullets for concise supporting points. Use tables sparingly and only when they make comparison clearer. Avoid long traceability matrices, filler checklists, decorative sections, and repeated boilerplate.

Good report sections include:

- Executive Summary
- What the Project Does
- Architecture Assessment
- Converter or System Quality
- Current Strengths
- Current Limitations
- Recommended Next Steps
- Owner Review Notes

For usage documentation, keep it practical:

- Install
- Convert a single file
- Convert a directory
- Style presets
- Writing Guidance

The `mdx` converter treats this leading title block as report metadata and builds a DOCX cover page from it automatically. The cover page layout follows a professional visual hierarchy:

1. **Thick accent rule** across the top of the page.
2. **Title** — large, bold, left-aligned (32 pt, preset heading font).
3. **Subtitle** — the `Document Type` field is pulled out and rendered as a 14 pt italic line beneath the title, in the preset heading color.
4. **Separator rule** — thin accent line below the title/subtitle block.
5. **Metadata table** — all remaining fields (`Project`, `Version`, `Author`, `Date`, `Status`, etc.) appear in a borderless two-column table. The left column (bold label) is 1.5 in wide; the right column (value) is 4.5 in wide. This replaces tab-aligned paragraphs and ensures consistent alignment regardless of label length.

Only `Document Type` is treated as the subtitle. All other fields appear in the table in the order they appear in the Markdown. Field names are rendered verbatim — use concise, title-case labels.

### Inline Formatting Support

The converter faithfully reproduces all standard inline formatting:

| Markdown syntax | Output |
|-----------------|--------|
| `**bold**` | Bold runs |
| `*italic*` or `_italic_` | Italic runs |
| `` `code` `` | Monospace with background shading |
| `[link](url)` | Underlined, colored hyperlink text |
| `~~strikethrough~~` | Struck-through run |

### Lists

Nested lists up to three levels deep map to proper Word list styles (`List Bullet`, `List Bullet 2`, `List Bullet 3`, etc.):

```md
- Top-level item
  - Second-level item
    - Third-level item
1. Ordered top-level
   1. Ordered second-level
```

### Tables

All inline formatting inside table cells is preserved — bold, italic, and inline code in table cells all survive conversion. Header cells are automatically bolded and shaded. Use tables only when columnar comparison adds genuine clarity.

### Code Blocks

Fenced code blocks render with monospace font, a background fill, and a colored left-border accent matched to the chosen style preset.

### Blockquotes

Blockquotes use an italic, indented style with a colored left-border accent:

```md
> This is a callout or important note.
```

### Images

Inline images cannot be embedded without the source file. The converter renders a descriptive placeholder (`[Image: alt text]`) so document content is never silently lost.

## Style Presets

The `--style` flag selects a typography and color scheme. All presets use widely available fonts. Table headers use dark fills with white text for professional, technical, executive, and minimal; academic uses a light grey fill with dark text.

| Preset | Body font | Heading font | Line spacing | Best for |
|--------|-----------|--------------|--------------|----------|
| `professional` | Calibri 11pt | Calibri Light | 1.3× | Client deliverables, consulting reports |
| `technical` | Segoe UI 10pt | Segoe UI | 1.25× | Internal technical specs, architecture docs |
| `executive` | Georgia 11pt | Georgia | 1.3× | Board-level summaries, executive briefings |
| `academic` | Times New Roman 12pt | Times New Roman | 2.0× | Research papers, formal academic writing |
| `minimal` | Arial 10pt | Arial | 1.15× | Internal memos, quick reference docs |

Default: `professional`.

## Conversion Workflow

Convert a single file (outputs `.docx` alongside the source):

```bash
mdx convert docs/engineering-report.md
```

With explicit output path:

```bash
mdx convert docs/engineering-report.md --output docs/engineering-report.docx
```

Convert an entire directory at once:

```bash
mdx convert docs/ --style professional --force
```

Check the installed version:

```bash
mdx version
```

Before finishing, verify that DOCX files open with `python-docx` and check at least title metadata, page size, header text, table count, and paragraph count.

## Avoid

- Placeholder words: TODO, TBD, FIXME.
- Personal emails or private identifiers.
- Unsupported security, compliance, or production-readiness claims.
- Mermaid diagrams — the converter does not render them as images; they appear as code blocks.
- Excessive tables — use them only when columnar comparison adds genuine clarity.

## Final Response

Return a concise summary with:

- Files created or updated.
- Validation commands run.
- DOCX files generated.
- Any owner-review caveats or known limitations.
