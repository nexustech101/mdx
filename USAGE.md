# MDX CLI Usage

`mdx` converts Markdown reports into professional DOCX documents. The recommended layout is simple: keep Markdown sources and generated DOCX files together in `docs`.

## Install

```bash
pip install .
mdx version
```

## Recommended Workflow

```bash
mdx init --with-template
mdx validate docs --strict
mdx batch docs --output-dir docs --style professional --force
mdx doctor
```

## Commands

### `mdx init`

Create the standard local project scaffold:

```bash
mdx init --with-template
```

This creates `mdx.toml`, `templates/professional.docx`, and `docs`.

### `mdx convert`

Convert one Markdown file:

```bash
mdx convert docs/engineering-report.md --output docs/engineering-report.docx --style professional --force
```

Useful flags:

- `--style professional|technical|executive|academic|minimal`
- `--template templates/professional.docx`
- `--strict`
- `--dry-run`
- `--verbose`
- `--quiet`

### `mdx batch`

Convert a folder of Markdown files:

```bash
mdx batch docs --output-dir docs --style professional --force
```

Use `--include` and `--exclude` to control which Markdown files are converted.

### `mdx validate`

Validate a Markdown file or folder:

```bash
mdx validate docs --strict
```

Optional checks include `--check-pii`, `--check-placeholders`, `--check-tables`, `--check-headings`, and `--check-links`.

### `mdx preview`

Generate an HTML preview:

```bash
mdx preview docs/engineering-report.md --output docs/engineering-report.html --style professional --force
```

### `mdx doctor`

Check local readiness:

```bash
mdx doctor
```

Required readiness depends on Python, `python-docx`, and `markdown-it-py`. Mermaid and Pandoc are optional checks.

## Writing Guidance

Professional MDX documents should be evidence-backed and concise. Use narrative analysis for engineering judgment, bullets for short lists, and tables only when they make comparison easier. A report-style document can start with a title and metadata block; the converter turns that into a DOCX cover page.

```md
# Engineering Report

**Project:** Example Project  
**Document Type:** Engineering Report  
**Version:** 1.0  
**Author:** Owner  
**Date:** 2026-05-11  
**Status:** Draft for review  

---
```

## Exit Codes

- `0`: success
- `1`: general error
- `2`: invalid command or arguments
- `3`: validation failed
- `4`: input path not found
- `5`: output path error
- `6`: template or config error
- `7`: conversion backend error
