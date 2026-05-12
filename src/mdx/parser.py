"""Shared parsing types and Markdown header extraction.

This module is import-free of any output-format library (docx, pdf, html).
Both :mod:`docx_converter` and :mod:`pdf_converter` depend on it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConvertResult:
    """Returned by every converter after a successful conversion."""

    input_path: Path
    output_path: Path
    style: str


@dataclass(frozen=True)
class ReportHeader:
    """Structured representation of a Markdown document's leading metadata block.

    The block is the H1 title followed by ``**Key:** Value`` lines terminated
    by a ``---`` rule::

        # Document Title

        **Project:** My Project
        **Document Type:** Engineering Report
        **Version:** 1.0
        **Date:** 2026-05-11

        ---

    If no conforming block is found the title may still be populated from the
    H1 while *metadata* will be empty and *body_markdown* will be the full
    original text.
    """

    title: str
    metadata: tuple[tuple[str, str], ...]
    body_markdown: str


_METADATA_RE = re.compile(r"^\*\*(.+?):\*\*\s*(.+?)\s*$")


def extract_report_header(markdown: str) -> ReportHeader:
    """Parse the leading title-and-metadata block from *markdown*.

    Returns a :class:`ReportHeader` whose *body_markdown* contains only the
    content that follows the ``---`` separator, ready for the renderer.
    """
    lines = markdown.splitlines()
    title = ""
    title_index: int | None = None

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            title_index = index
            break

    if title_index is None:
        return ReportHeader(title="", metadata=(), body_markdown=markdown)

    metadata: list[tuple[str, str]] = []
    end_index: int | None = None

    for index in range(title_index + 1, min(len(lines), title_index + 12)):
        stripped = lines[index].strip()
        if stripped == "---":
            end_index = index + 1
            break
        if not stripped:
            continue
        match = _METADATA_RE.match(stripped)
        if not match:
            break
        metadata.append((match.group(1), match.group(2).strip()))

    if not metadata or end_index is None:
        return ReportHeader(title=title, metadata=(), body_markdown=markdown)

    body = "\n".join(lines[end_index:]).lstrip()
    return ReportHeader(title=title, metadata=tuple(metadata), body_markdown=body)
