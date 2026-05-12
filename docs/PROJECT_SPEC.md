# Project Specification

**Project:** mdx-cli
**Document Type:** Technical Project Specification
**Version:** 1.0
**Date:** 2026-05-11
**Status:** Draft for Owner Review

---

## Purpose and Goals

`mdx-cli` is a Python command-line tool that converts Markdown files into professionally formatted DOCX and PDF documents. It is designed for engineers and technical writers who produce reports, specifications, and proposals in Markdown and need polished Word-compatible output without manually formatting documents. The tool targets repeatability: the same Markdown source plus the same style preset always produces the same output.

## System Overview

- **Architecture:** Single-package CLI application. No web server, no database, no daemon.
- **Languages and frameworks:** Python 3.11+. CLI built on `registers`. DOCX generation via `python-docx`. Markdown tokenisation via `markdown-it-py`. PDF conversion via `docx2pdf` (delegates to Microsoft Word on Windows/macOS or LibreOffice on Linux).
- **Runtime:** Installed as an editable package into a virtual environment. Exposed as the `mdx` script via `[project.scripts]` in `pyproject.toml`.
- **Deployment:** Local developer machine. No containerisation, no CI pipeline currently present.

## Module Inventory

| Module | Description |
|---|---|
| `cli.py` | Entry point. Registers `docx`, `pdf`, and `version` commands. Contains `_run_conversion()`, the shared file/directory dispatch helper. |
| `parser.py` | Format-agnostic shared types. Defines `ConvertResult` and `ReportHeader` dataclasses. Implements `extract_report_header()` for parsing the leading metadata block from Markdown. No output-format imports. |
| `docx_converter.py` | Markdown-to-DOCX renderer. Tokenises Markdown with `markdown-it-py` and walks tokens to build a `python-docx` document. Contains all OOXML helpers. |
| `pdf_converter.py` | Thin Markdown-to-PDF adapter. Produces a temporary DOCX via `docx_converter`, converts it with `docx2pdf`, then deletes the temp file. |
| `styles.py` | `StylePreset` frozen dataclass, `STYLE_PRESETS` dictionary, `apply_document_style()`, `get_style_preset()`, and `rgb_hex()` colour utility. |
| `config.py` | `mdx.toml` loader. Defines `DEFAULT_CONFIG`, `deep_merge()`, and `load_config()`. |
| `validation.py` | Pre-conversion Markdown linter. Detects heading order violations, placeholder tokens, PII patterns, broken links, and empty tables. Returns structured `ValidationReport` objects. |
| `__init__.py` | Package version (`__version__ = "0.1.0"`). |

## Data Model

### `ConvertResult`

Frozen dataclass returned by every converter after a successful conversion.

| Field | Type | Description |
|---|---|---|
| `input_path` | `Path` | Source Markdown file |
| `output_path` | `Path` | Generated output file |
| `style` | `str` | Resolved style preset name |

### `ReportHeader`

Frozen dataclass representing the parsed leading metadata block of a Markdown document.

| Field | Type | Description |
|---|---|---|
| `title` | `str` | Text of the H1 heading |
| `metadata` | `tuple[tuple[str, str], ...]` | Ordered key-value pairs from `**Key:** Value` lines |
| `body_markdown` | `str` | Document body after the `---` separator |

### `StylePreset`

Frozen dataclass describing a typography and colour theme.

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Preset identifier |
| `body_font` | `str` | Body text font family |
| `body_size` | `int` | Body font size in points |
| `heading_font` | `str` | Heading font family |
| `heading_color` | `tuple[int, int, int]` | Heading RGB colour |
| `accent_color` | `tuple[int, int, int]` | Accent / border RGB colour |
| `table_header_fill` | `str` | Table header background hex |
| `code_fill` | `str` | Code block background hex |
| `code_font` | `str` | Code block font family |
| `line_spacing` | `float` | Body line spacing multiplier |
| `header_text_color` | `str` | Table header text colour hex |

### `ValidationIssue`

| Field | Type | Description |
|---|---|---|
| `severity` | `str` | `"warning"` or `"error"` |
| `message` | `str` | Human-readable description |
| `line` | `int \| None` | Source line number, if applicable |

### `ValidationReport`

| Field / Property | Type | Description |
|---|---|---|
| `path` | `Path` | Validated file |
| `issues` | `tuple[ValidationIssue, ...]` | All issues found |
| `warnings` | `int` (property) | Count of warning-severity issues |
| `errors` | `int` (property) | Count of error-severity issues |
| `passed` | `bool` (property) | `True` when `errors == 0` |

## CLI Surface

Entry point: `mdx` (installed via `[project.scripts]`).

| Command | Arguments | Description |
|---|---|---|
| `mdx docx <input>` | `--output`, `--style`, `--force`, `--quiet` | Convert Markdown file or directory to DOCX |
| `mdx pdf <input>` | `--output`, `--style`, `--force`, `--quiet` | Convert Markdown file or directory to PDF |
| `mdx version` | _(none)_ | Print installed package version |

### Shared flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `--output` | `str` | Alongside source | Output file path or directory |
| `--style` | `str` | `professional` (or from `mdx.toml`) | Style preset name |
| `--force` | `bool` | `False` | Overwrite existing output files |
| `--quiet` | `bool` | `False` | Suppress all stdout output |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 4 | Input file or directory not found |
| 5 | Output path conflict |
| 6 | Template or configuration error |
| 7 | Conversion backend error |

## Third-Party Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `registers[cli]` | `>=0.2.0` | `CommandRegistry` — CLI command and argument registration |
| `python-docx` | `>=1.1.2` | DOCX document creation and OOXML manipulation |
| `markdown-it-py` | `>=3.0.0` | Markdown tokeniser used by the DOCX renderer |
| `docx2pdf` | `>=0.1.8` | DOCX-to-PDF conversion via Microsoft Word / LibreOffice |
| `setuptools` | `>=69` (build only) | Package build backend |

All runtime dependencies are declared in `pyproject.toml` under `[project.dependencies]`.

## Configuration

Configuration is loaded from `mdx.toml` in the working directory. The file is optional; defaults are applied for every missing key.

```toml
[project]
name   = "MDX Project"
author = ""

[output]
directory = "docs"
overwrite  = false

[style]
preset   = "professional"   # professional | technical | executive | academic | minimal
template = ""               # optional .docx template path

[document]
page_size    = "letter"
margins      = "normal"
toc          = true
page_numbers = true
headers      = true
footers      = true
cover_page   = false

[markdown]
enable_tables      = true
enable_footnotes   = true
enable_mermaid     = true
enable_toc         = true
enable_code_blocks = true

[validation]
strict              = false
check_placeholders  = true
check_pii           = false
check_heading_order = true
check_empty_tables  = true
check_links         = false
```

The CLI reads only `[style].preset` from the config at runtime. All other keys are defined in `DEFAULT_CONFIG` for future feature use.

## Testing Strategy

No automated test suite is currently present. Regression testing has been performed manually:

- Smoke tests: `mdx docx` and `mdx pdf` run against `examples/software-development-agreement.md` with `--force` and produce valid output files.
- Structural regression: SHA-256 of `word/document.xml` inside the DOCX ZIP (`9250b07c1c976160024da99fe9a5d5a62fe9ee389690b7d696c2e3d452e74e8b`) is used as a baseline for future comparison.
- Type checking: Pylance reports no errors across all source modules.

## Known Limitations

- **No automated tests.** The project has no `pytest` suite. Any refactor relies on manual smoke tests.
- **PDF requires Word or LibreOffice.** `docx2pdf` delegates to a desktop office application. Headless or cloud environments require LibreOffice to be installed separately.
- **Images are not embedded.** The DOCX renderer replaces inline images with a placeholder string. Embedding binary image files is not yet implemented.
- **Mermaid diagrams are not rendered.** Fenced code blocks with the `mermaid` language tag are rendered as plain code blocks, not diagrams.
- **`mdx.toml` partially implemented.** Many config keys (`document.*`, `markdown.*`, `validation.*`) are read into the default config but are not yet plumbed into the converters.
- **`validation.py` is not wired to the CLI.** The `validate_markdown_file()` function exists and is tested in isolation but there is no `mdx validate` command.
- **Single-section documents only.** `apply_document_style()` operates on `document.sections[0]`. Multi-section layouts (e.g., landscape appendices) are not supported.

## Recommended Next Steps

1. **Add a `pytest` suite.** At minimum, parametrise `convert_markdown_to_docx` over all five style presets and assert the output file exists and is non-empty. Use `python-docx` to assert paragraph styles and font names.
2. **Wire `validation.py` to the CLI.** Add a `mdx validate <input>` command that runs `validate_markdown_file()` and prints issues, exiting non-zero on errors.
3. **Implement image embedding.** Accept local image paths relative to the Markdown source file and embed them using `docx.add_picture()`.
4. **Support `mdx.toml` `[document].cover_page`.** When `cover_page = false`, suppress cover page generation even for documents that have a metadata block.
5. **Headless PDF support.** Document the LibreOffice path for CI/server environments and add a `--pdf-engine` flag to select between Word and LibreOffice.
6. **Publish to PyPI.** The package is structured correctly for publication. Add a `[project.urls]` section and a GitHub Actions workflow for `pypi-publish`.
