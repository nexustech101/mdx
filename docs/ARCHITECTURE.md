# MDX Architecture

**Project:** mdx-cli
**Document Type:** Architecture Overview
**Version:** 1.0
**Date:** 2026-05-11
**Status:** Current

---

## Overview

`mdx-cli` is a Python command-line tool that converts Markdown documents into professionally formatted DOCX and PDF files. The codebase is organised around a strict three-layer architecture: a format-agnostic parsing layer, a DOCX rendering layer, and a thin PDF adapter that reuses the DOCX layer rather than duplicating styling logic.

## Module Map

```
src/mdx/
├── __init__.py          # Package version
├── cli.py               # Entry point — CommandRegistry, docx/pdf/version commands
├── parser.py            # Shared types and Markdown header extraction (no format deps)
├── docx_converter.py    # Markdown → DOCX via python-docx + markdown-it-py
├── pdf_converter.py     # Markdown → PDF via docx_converter + docx2pdf
├── styles.py            # StylePreset dataclass, STYLE_PRESETS registry, apply_document_style()
├── config.py            # mdx.toml loader with deep-merge defaults
└── validation.py        # Pre-conversion Markdown linting
```

## Dependency Graph

```
cli.py
 ├── docx_converter.py
 │    ├── parser.py          (ConvertResult, ReportHeader, extract_report_header)
 │    └── styles.py          (StylePreset, apply_document_style, rgb_hex)
 └── pdf_converter.py
      ├── docx_converter.py  (convert_markdown_to_docx — reused, not duplicated)
      └── parser.py          (ConvertResult)
```

`parser.py` has no output-format imports. It depends only on the Python standard library, making it safe to import from both converters without creating circular dependencies.

## Data Flow

### DOCX conversion

```
.md file
  → cli._run_conversion()
  → docx_converter.convert_markdown_to_docx()
      → parser.extract_report_header()   [splits cover metadata from body]
      → styles.apply_document_style()    [page geometry + Word styles]
      → docx_converter._add_cover_page() [accent bar, title, metadata table]
      → docx_converter._apply_report_header_footer()
      → docx_converter._render_markdown() [token-by-token OOXML rendering]
      → document.save()
  → ConvertResult
```

### PDF conversion

```
.md file
  → cli._run_conversion()
  → pdf_converter.convert_markdown_to_pdf()
      → tempfile.NamedTemporaryFile(suffix=".docx")
      → docx_converter.convert_markdown_to_docx()  [full DOCX pipeline above]
      → docx2pdf.convert(tmp_docx, output_pdf)     [delegates to Word / LibreOffice]
      → tmp_docx.unlink()
  → ConvertResult
```

The PDF output is guaranteed to be visually identical to the DOCX because it is produced from the same intermediate file with no separate styling path.

## Rendering Pipeline

`docx_converter._render_markdown()` uses `markdown-it-py` to tokenise the Markdown source and processes tokens with a state machine. The renderer handles:

| Token type | Output |
|---|---|
| `heading_open` / `heading_close` | Word `Heading 1`–`Heading 6` styles |
| `paragraph_open` / `paragraph_close` | Word `Normal` paragraph |
| `inline` (with children) | Run-level formatting via `_append_inline()` |
| `bullet_list`, `ordered_list` | Word `List Bullet` / `List Number` 1–3 |
| `table` | `_render_table()` with shaded header row |
| `fence` | Code block: monospace, filled background, coloured left border |
| `blockquote` | Italic, indented, coloured left border |
| `hr` | Thin full-width rule via OOXML `pBdr` |
| `html_block` | `<!-- pagebreak -->` detected and converted to Word page break |
| `image` | Descriptive placeholder `[Image: alt text]` (no file embed) |

Inline tokens handled within `_append_inline()`:

| Token | Effect |
|---|---|
| `strong_open` | `run.bold = True` |
| `em_open` | `run.italic = True` |
| `code_inline` | Monospace font + background shading via OOXML `rPr` |
| `link_open` | Underline + accent colour |
| `s_open` | `run.font.strike = True` |
| `softbreak` | Space character |

## Cover Page

When the leading block of a Markdown document matches the metadata format below, `_add_cover_page()` generates a formatted cover page before the body content.

```md
# Document Title

**Project:** My Project
**Document Type:** Engineering Report
**Version:** 1.0
**Date:** 2026-05-11

---
```

The cover page consists of:

1. A full-width accent-coloured bar (`_shade_paragraph()`).
2. Title paragraph in large heading font.
3. An italic subtitle from the `Document Type` metadata field (if present).
4. A thin separator rule (`_set_paragraph_bottom_border()`).
5. A borderless two-column table of the remaining metadata key-value pairs.
6. A page break before the document body.

Running headers (`_apply_report_header_footer()`) insert the document title right-aligned in the header and centred page numbers in the footer using OOXML `fldChar` fields.

## Style System

Styles are defined as frozen `StylePreset` dataclasses in `styles.py`. `apply_document_style()` sets page geometry (letter, 1.25-inch side margins) and configures Word paragraph styles (`Normal`, `Heading 1`–`6`, `List Bullet` 1–3, `List Number` 1–3) by modifying existing styles rather than creating new ones, ensuring compatibility with templates.

| Preset | Body font | Size | Line spacing | Primary use |
|---|---|---|---|---|
| `professional` | Calibri | 11 pt | 1.3× | Client deliverables |
| `technical` | Segoe UI | 10 pt | 1.25× | Internal technical docs |
| `executive` | Georgia | 11 pt | 1.3× | Board-level briefings |
| `academic` | Times New Roman | 12 pt | 2.0× | Research papers |
| `minimal` | Arial | 10 pt | 1.15× | Internal memos |

## Configuration

`cli._resolve_style()` consults `mdx.toml` in the working directory when no `--style` flag is passed. The file is parsed by `config.load_config()`, which deep-merges user-provided keys over `DEFAULT_CONFIG`. All keys are optional; defaults are applied for any missing key.

```toml
[style]
preset = "professional"

[output]
directory = "docs"
overwrite  = false
```

## CLI Architecture

The CLI is built on the `registers` library (`CommandRegistry`). Commands are registered with `@registry.register` and arguments with `@registry.argument`. The entry point `mdx.cli:main` is declared in `pyproject.toml` under `[project.scripts]`.

`_run_conversion()` is a shared internal helper used by both `docx` and `pdf` commands. It handles file-vs-directory branching, output path resolution, and per-file error handling. The only difference between the two commands is the `suffix` argument (`.docx` or `.pdf`) passed to `_run_conversion()`, which selects the converter callable.

## Error Handling

All user-facing errors exit via `_error()`, which prints to stderr and raises `SystemExit` with a numeric code. No exceptions propagate to the terminal.

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 4 | Input file or directory not found |
| 5 | Output path conflict (use `--force` to override) |
| 6 | Template or configuration error |
| 7 | Conversion backend error |

## Key Design Decisions

**No duplicate styling logic.** PDF output is produced by converting the intermediate DOCX, not by running a parallel Markdown renderer. Any fix to the DOCX renderer automatically applies to PDF.

**Format-agnostic parser.** `parser.py` imports nothing from `docx` or `docx2pdf`, keeping shared types decoupled from output formats. This boundary is enforced by the module docstring.

**Styles are data, not code.** `StylePreset` is a frozen dataclass. Adding a new preset requires no new functions — only a new entry in `STYLE_PRESETS`.

**Graceful cover page detection.** The metadata block parser (`extract_report_header`) is lenient: if the leading block does not conform, the full Markdown is passed to the renderer unchanged and no cover page is generated. Files without metadata headers convert correctly.
