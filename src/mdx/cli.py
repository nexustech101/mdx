from __future__ import annotations

import sys
from pathlib import Path

from registers import CommandRegistry
from registers.cli import types as t

from . import __version__
from .config import load_config
from .converter import convert_markdown_to_docx
from .styles import STYLE_PRESETS

EXIT_OK = 0
EXIT_GENERAL = 1
EXIT_ARGS = 2
EXIT_INPUT_NOT_FOUND = 4
EXIT_OUTPUT_PATH = 5
EXIT_CONFIG_OR_TEMPLATE = 6
EXIT_BACKEND = 7

registry = CommandRegistry()


def _error(message: str, *, code: int, path: Path | None = None, hint: str | None = None) -> None:
    print(f"Error: {message}", file=sys.stderr)
    if path is not None:
        print("\nPath:", file=sys.stderr)
        print(path, file=sys.stderr)
    if hint:
        print(f"\n{hint}", file=sys.stderr)
    raise SystemExit(code)


def _log(message: str, *, quiet: bool = False) -> None:
    if not quiet:
        print(message)


def _ensure_write_target(path: Path, *, force: bool) -> None:
    if path.exists() and not force:
        _error(
            "output file already exists.",
            code=EXIT_OUTPUT_PATH,
            path=path,
            hint="Use --force to overwrite.",
        )
    path.parent.mkdir(parents=True, exist_ok=True)


def _resolve_style(style: str | None) -> str:
    if not style:
        config_path = Path("mdx.toml")
        if config_path.exists():
            try:
                cfg = load_config(config_path, explicit=False)
                style = cfg.get("style", {}).get("preset") or ""
            except Exception:
                pass
    resolved = (style or "professional").strip().lower()
    if resolved not in STYLE_PRESETS:
        _error(
            f"unsupported style '{resolved}'.",
            code=EXIT_ARGS,
            hint=f"Use one of: {', '.join(STYLE_PRESETS)}.",
        )
    return resolved


def _discover_markdown_files(input_dir: Path) -> list[Path]:
    return sorted(p for p in input_dir.rglob("*.md") if p.is_file())


@registry.register(
    "convert",
    description="Convert a Markdown file or directory to DOCX.",
    examples=[
        "mdx convert report.md",
        "mdx convert docs/",
        "mdx convert report.md --output report.docx",
        "mdx convert docs/ --style technical --force",
    ],
    render=False,
)
@registry.argument("input", type=t.Path(exists=True), help="Markdown file or directory.")
@registry.argument("output", type=str, default="", help="Output .docx file or directory (default: alongside source).")
@registry.argument("style", type=str, default="", help="Style preset: professional, technical, executive, academic, minimal.")
@registry.argument("force", type=bool, default=False, help="Overwrite existing output files.")
@registry.argument("quiet", type=bool, default=False, help="Suppress output.")
def convert(
    input: Path,
    output: str = "",
    style: str = "",
    force: bool = False,
    quiet: bool = False,
) -> None:
    source = Path(input)
    resolved_style = _resolve_style(style or None)

    if source.is_file():
        out = Path(output) if output else source.with_suffix(".docx")
        _ensure_write_target(out, force=force)
        try:
            convert_markdown_to_docx(source, out, style=resolved_style)
        except Exception as exc:
            _error(f"conversion failed: {exc}", code=EXIT_BACKEND)
        _log(f"{source.as_posix()} -> {out.as_posix()}", quiet=quiet)

    else:
        out_root = Path(output) if output else source
        files = _discover_markdown_files(source)
        if not files:
            _error("no Markdown files found.", code=EXIT_INPUT_NOT_FOUND, path=source)
        converted = 0
        for md_file in files:
            dest = out_root / md_file.relative_to(source).with_suffix(".docx")
            _ensure_write_target(dest, force=force)
            try:
                convert_markdown_to_docx(md_file, dest, style=resolved_style)
            except Exception as exc:
                _error(f"conversion failed: {exc}", code=EXIT_BACKEND, path=md_file)
            converted += 1
            _log(f"{md_file.as_posix()} -> {dest.as_posix()}", quiet=quiet)
        _log(f"\n{converted} file(s) converted.", quiet=quiet)



@registry.register("version", description="Show installed version.")
def version() -> str:
    return f"mdx {__version__}"


def main() -> None:
    try:
        registry.run(shell_title="MDX CLI", shell_usage=True)
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover - catch-all guard
        _error(str(exc), code=EXIT_GENERAL)


if __name__ == "__main__":
    main()
