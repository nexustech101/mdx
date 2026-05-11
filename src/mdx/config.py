from __future__ import annotations

import copy
import tomllib
from pathlib import Path
from typing import Any

DEFAULT_CONFIG: dict[str, Any] = {
    "project": {"name": "MDX Project", "author": ""},
    "output": {"directory": "docs", "overwrite": False},
    "style": {"preset": "professional", "template": ""},
    "document": {
        "page_size": "letter",
        "margins": "normal",
        "toc": True,
        "page_numbers": True,
        "headers": True,
        "footers": True,
        "cover_page": False,
    },
    "markdown": {
        "enable_tables": True,
        "enable_footnotes": True,
        "enable_mermaid": True,
        "enable_toc": True,
        "enable_code_blocks": True,
    },
    "validation": {
        "strict": False,
        "check_placeholders": True,
        "check_pii": False,
        "check_heading_order": True,
        "check_empty_tables": True,
        "check_links": False,
    },
}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: Path | None, *, explicit: bool = False) -> dict[str, Any]:
    if path is None:
        return copy.deepcopy(DEFAULT_CONFIG)

    if not path.exists():
        if explicit:
            raise FileNotFoundError(f"Configuration file not found: {path}")
        return copy.deepcopy(DEFAULT_CONFIG)

    try:
        with path.open("rb") as handle:
            parsed = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"Invalid TOML in configuration file {path}: {exc}") from exc

    return deep_merge(DEFAULT_CONFIG, parsed)


def write_default_config(path: Path, *, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(path)

    content = """[project]
name = "Software Documentation Bundle"
author = "Your Name"

[output]
directory = "docs"
overwrite = true

[style]
preset = "professional"
template = "templates/professional.docx"

[document]
page_size = "letter"
margins = "normal"
toc = true
page_numbers = true
headers = true
footers = true
cover_page = true

[markdown]
enable_tables = true
enable_footnotes = true
enable_mermaid = true
enable_toc = true
enable_code_blocks = true

[validation]
strict = true
check_placeholders = true
check_pii = true
check_heading_order = true
check_empty_tables = true
check_links = true
"""
    path.write_text(content, encoding="utf-8")
