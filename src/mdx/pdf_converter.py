"""Markdown or DOCX → PDF converter.

Accepts either a Markdown (``.md``) or an already-rendered DOCX (``.docx``) file
as input and produces a PDF via ``docx2pdf``.

- **Markdown input:** converted to a temporary DOCX via :func:`convert_markdown_to_docx`,
  then the DOCX is handed to ``docx2pdf``.  The intermediate file is deleted after
  conversion.  The PDF is therefore visually identical to running ``mdx docx`` first.
- **DOCX input:** passed directly to ``docx2pdf`` with no intermediate step.

Requires Microsoft Word on Windows/macOS, or LibreOffice on Linux.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from docx2pdf import convert as _docx2pdf

from .docx_converter import convert_markdown_to_docx
from .parser import ConvertResult


def convert_markdown_to_pdf(
    input_path: Path,
    output_path: Path,
    *,
    style: str,
    template_path: Path | None = None,
) -> ConvertResult:
    """Convert *input_path* (Markdown or DOCX) to *output_path* (PDF).

    If *input_path* has a ``.docx`` extension it is passed directly to
    ``docx2pdf`` without a Markdown conversion step.  Otherwise the full
    Markdown → DOCX → PDF pipeline is used.

    Args:
        input_path:    Source ``.md`` or ``.docx`` file.
        output_path:   Destination ``.pdf`` file.  Parent directories are
                       created automatically.
        style:         Name of a :data:`~styles.STYLE_PRESETS` key (used only
                       when *input_path* is a Markdown file).
        template_path: Optional ``.docx`` template passed through to the DOCX
                       converter (Markdown input only).

    Returns:
        A :class:`~parser.ConvertResult` with paths and the resolved style name.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if input_path.suffix.lower() == ".docx":
        # Input is already a DOCX — convert directly, no Markdown step needed.
        _docx2pdf(str(input_path), str(output_path))
        return ConvertResult(input_path=input_path, output_path=output_path, style=style)

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp_docx = Path(tmp.name)

    try:
        convert_markdown_to_docx(
            input_path,
            tmp_docx,
            style=style,
            template_path=template_path,
        )
        _docx2pdf(str(tmp_docx), str(output_path))
    finally:
        tmp_docx.unlink(missing_ok=True)

    return ConvertResult(input_path=input_path, output_path=output_path, style=style)
