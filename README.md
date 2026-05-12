# mdx

`mdx` is a command-line tool for converting Markdown files into polished DOCX and PDF documents.

## Install

```bash
pip install .
```

## Quickstart

```bash
# Convert to DOCX
mdx docx report.md

# Convert to PDF (requires Microsoft Word)
mdx pdf report.md

# Convert a whole directory
mdx docx docs/ --style professional --force
```
