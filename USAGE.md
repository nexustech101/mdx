# MDX CLI Usage

`mdx` converts Markdown reports into professional DOCX and PDF documents.

## Install

```bash
pip install .
```

## Convert to DOCX

Convert a single file (output defaults to `report.docx` alongside the source):

```bash
mdx docx report.md
```

Override the output path with `--output`:

```bash
mdx docx report.md --output docs/report.docx
```

Convert every `.md` file in a directory:

```bash
mdx docx docs/
```

## Convert to PDF

Convert a single file (output defaults to `report.pdf` alongside the source):

```bash
mdx pdf report.md
```

Convert every `.md` file in a directory:

```bash
mdx pdf docs/
```

PDF output is rendered via Microsoft Word, so it is visually identical to the DOCX output. Word must be installed for PDF conversion.

## Options

Both `mdx docx` and `mdx pdf` accept the same flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--output` | alongside source | Output file or directory |
| `--style` | `professional` | Style preset |
| `--force` | off | Overwrite existing output files |
| `--quiet` | off | Suppress output |

## Style presets

```bash
mdx docx report.md --style technical
```

Available: `professional`, `technical`, `executive`, `academic`, `minimal`.

## Check version

```bash
mdx version
```

## Exit codes

- `0` success
- `1` general error
- `2` invalid arguments
- `4` input not found
- `5` output path error
- `6` template or config error
- `7` conversion backend error

