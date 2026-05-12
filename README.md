# mdx

A command-line tool that converts Markdown files into professionally formatted **DOCX** and **PDF** documents — with cover pages, running headers and footers, styled tables, code blocks, and five built-in typography presets.

## Features

- **Cover page generation** — H1 title, italic document type sub-heading, and key-value metadata parsed directly from the Markdown header block
- **Five style presets** — `professional`, `technical`, `executive`, `academic`, `minimal`
- **Full Markdown support** — headings, paragraphs, bold/italic/code inline, bullet and numbered lists (3 levels deep), tables, fenced code blocks, blockquotes, horizontal rules, and page break comments
- **Running headers and footers** — document title in the header, page numbers in the footer
- **DOCX and PDF output** — PDF is rendered via Microsoft Word so it is pixel-perfect with the DOCX
- **File or directory input** — convert a single file or every `.md` file in a directory tree in one command
- **Per-project config** — default style and output directory settable in `mdx.toml`

## Requirements

- Python 3.11+
- Microsoft Word (Windows or macOS) for PDF output — not required for DOCX

## Install

```bash
pip install .
```

For an editable development install:

```bash
pip install -e .
```

## Quickstart

```bash
# Convert to DOCX
mdx docx report.md

# Convert to PDF
mdx pdf report.md

# Override output path
mdx docx report.md --output dist/report.docx

# Convert every .md file in a directory
mdx docx docs/ --style technical --force
```

## Document Format

Place a metadata block at the top of any Markdown file to generate a cover page automatically:

```markdown
# Document Title

**Project:** My Project
**Document Type:** Engineering Report
**Version:** 1.0
**Date:** 2026-05-11
**Status:** Draft

---

Body content starts here...
```

Any `**Key:** Value` lines between the H1 and the `---` separator are rendered as cover page metadata. The `Document Type` field becomes the italic sub-heading beneath the title.

## Commands

### `mdx docx`

Convert a Markdown file or directory to DOCX.

```
mdx docx <input> [--output PATH] [--style PRESET] [--force] [--quiet]
```

### `mdx pdf`

Convert a Markdown file or directory to PDF.

```
mdx pdf <input> [--output PATH] [--style PRESET] [--force] [--quiet]
```

### `mdx version`

Print the installed version.

### Options

| Flag | Default | Description |
|---|---|---|
| `--output` | Alongside source | Output file or directory |
| `--style` | `professional` | Style preset name |
| `--force` | off | Overwrite existing output files |
| `--quiet` | off | Suppress all stdout output |

## Style Presets

| Preset | Body font | Size | Spacing | Best for |
|---|---|---|---|---|
| `professional` | Calibri | 11 pt | 1.3× | Client deliverables, consulting reports |
| `technical` | Segoe UI | 10 pt | 1.25× | Internal specs, architecture docs |
| `executive` | Georgia | 11 pt | 1.3× | Board summaries, executive briefings |
| `academic` | Times New Roman | 12 pt | 2.0× | Research papers, formal writing |
| `minimal` | Arial | 10 pt | 1.15× | Internal memos, quick-reference docs |

## Configuration

Create an `mdx.toml` file in your project root to set defaults:

```toml
[style]
preset = "professional"

[output]
directory = "docs"
overwrite  = false
```

The `--style` flag always takes precedence over the config file.

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 4 | Input file or directory not found |
| 5 | Output path conflict (use `--force`) |
| 6 | Template or configuration error |
| 7 | Conversion backend error |

## Project Structure

```
src/mdx/
├── cli.py               # Entry point — docx, pdf, version commands
├── parser.py            # Shared types and Markdown header extraction
├── docx_converter.py    # Markdown → DOCX renderer
├── pdf_converter.py     # Markdown → PDF (via docx_converter + docx2pdf)
├── styles.py            # Style presets and document style application
├── config.py            # mdx.toml loader
└── validation.py        # Pre-conversion Markdown linter
```

See [docs/architecture.md](docs/architecture.md) for a full architecture overview and [docs/project-spec.md](docs/project-spec.md) for the complete project specification.

