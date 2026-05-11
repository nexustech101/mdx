# MDX CLI Usage

`mdx` converts Markdown reports into professional DOCX documents.

## Install

```bash
pip install .
```

## Convert a single file

```bash
mdx convert report.md
```

Output defaults to `report.docx` alongside the source. Override with `--output`:

```bash
mdx convert report.md --output docs/report.docx
```

## Convert a directory

```bash
mdx convert docs/
```

Converts every `.md` file in the directory to a `.docx` file alongside it.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--output` | alongside source | Output `.docx` file or directory |
| `--style` | `professional` | Style preset |
| `--force` | off | Overwrite existing output files |
| `--quiet` | off | Suppress output |

## Style presets

```bash
mdx convert report.md --style technical
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

