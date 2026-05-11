from __future__ import annotations

from dataclasses import dataclass

from docx.document import Document as DocumentType
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


@dataclass(frozen=True)
class StylePreset:
    name: str
    body_font: str
    body_size: int
    heading_font: str
    heading_color: tuple[int, int, int]
    accent_color: tuple[int, int, int]
    table_header_fill: str
    code_fill: str
    code_font: str
    line_spacing: float = 1.3
    header_text_color: str = "FFFFFF"


STYLE_PRESETS: dict[str, StylePreset] = {
    # Clean, modern consulting look — Calibri Light headings over Calibri body.
    "professional": StylePreset(
        name="professional",
        body_font="Calibri",
        body_size=11,
        heading_font="Calibri Light",
        heading_color=(31, 58, 95),    # deep navy
        accent_color=(43, 87, 154),    # royal blue
        table_header_fill="1F3A5F",
        code_fill="F2F4F7",
        code_font="Consolas",
        line_spacing=1.3,
    ),
    # High-density technical documentation — Segoe UI throughout.
    "technical": StylePreset(
        name="technical",
        body_font="Segoe UI",
        body_size=10,
        heading_font="Segoe UI",
        heading_color=(18, 18, 30),    # near-black navy
        accent_color=(22, 66, 128),    # dark blue
        table_header_fill="162D50",
        code_fill="F0F2F5",
        code_font="Consolas",
        line_spacing=1.25,
    ),
    # Formal client-facing reports — Georgia for a polished serif look.
    "executive": StylePreset(
        name="executive",
        body_font="Georgia",
        body_size=11,
        heading_font="Georgia",
        heading_color=(32, 32, 32),    # near-black
        accent_color=(100, 40, 130),   # deep purple
        table_header_fill="4A1A6E",
        code_fill="F8F6FF",
        code_font="Consolas",
        line_spacing=1.3,
    ),
    # Academic / research papers — Times New Roman double-spaced.
    "academic": StylePreset(
        name="academic",
        body_font="Times New Roman",
        body_size=12,
        heading_font="Times New Roman",
        heading_color=(0, 0, 0),
        accent_color=(70, 70, 70),
        table_header_fill="CCCCCC",
        code_fill="F8F8F8",
        code_font="Courier New",
        line_spacing=2.0,
        header_text_color="111111",
    ),
    # Stripped-back internal docs — Arial, no decoration.
    "minimal": StylePreset(
        name="minimal",
        body_font="Arial",
        body_size=10,
        heading_font="Arial",
        heading_color=(0, 0, 0),
        accent_color=(80, 80, 80),
        table_header_fill="333333",
        code_fill="F7F7F7",
        code_font="Consolas",
        line_spacing=1.15,
    ),
}


def rgb_hex(color: tuple[int, int, int]) -> str:
    """Return a six-character uppercase hex string for a (r, g, b) tuple."""
    return f"{color[0]:02X}{color[1]:02X}{color[2]:02X}"


def get_style_preset(name: str) -> StylePreset:
    lowered = name.strip().lower()
    if lowered not in STYLE_PRESETS:
        supported = ", ".join(STYLE_PRESETS.keys())
        raise ValueError(f"Unsupported style preset '{name}'. Supported styles: {supported}")
    return STYLE_PRESETS[lowered]


def apply_document_style(document: DocumentType, preset_name: str) -> StylePreset:
    preset = get_style_preset(preset_name)

    # ── Page geometry ────────────────────────────────────────────────────────
    section = document.sections[0]
    section.page_height = Inches(11)
    section.page_width = Inches(8.5)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.25)
    section.header_distance = Inches(0.5)
    section.footer_distance = Inches(0.5)

    # ── Normal (body) ────────────────────────────────────────────────────────
    normal = document.styles["Normal"]
    normal.font.name = preset.body_font
    normal.font.size = Pt(preset.body_size)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = preset.line_spacing

    # ── Headings ─────────────────────────────────────────────────────────────
    # (size_pt, bold, space_before_pt, space_after_pt)
    heading_specs: dict[int, tuple[int, bool, int, int]] = {
        1: (26, True,  24, 8),
        2: (18, True,  18, 6),
        3: (14, True,  14, 4),
        4: (12, True,  12, 2),
        5: (11, True,   8, 2),
        6: (10, False,  6, 2),
    }
    for level, (size, bold, sb, sa) in heading_specs.items():
        h = document.styles[f"Heading {level}"]
        h.font.name = preset.heading_font
        h.font.color.rgb = RGBColor(*preset.heading_color)
        h.font.size = Pt(size)
        h.font.bold = bold
        h.paragraph_format.keep_with_next = True
        h.paragraph_format.space_before = Pt(sb)
        h.paragraph_format.space_after = Pt(sa)

    # ── Title (cover page) ───────────────────────────────────────────────────
    title_style = document.styles["Title"]
    title_style.font.name = preset.heading_font
    title_style.font.color.rgb = RGBColor(*preset.heading_color)
    title_style.font.size = Pt(32)
    title_style.font.bold = True
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    title_style.paragraph_format.space_after = Pt(16)

    # ── Quote / blockquote ───────────────────────────────────────────────────
    quote_style = document.styles["Quote"]
    quote_style.font.name = preset.body_font
    quote_style.font.italic = True
    quote_style.font.color.rgb = RGBColor(80, 80, 80)
    quote_style.paragraph_format.left_indent = Inches(0.4)
    quote_style.paragraph_format.right_indent = Inches(0.2)
    quote_style.paragraph_format.space_before = Pt(6)
    quote_style.paragraph_format.space_after = Pt(6)

    # ── List styles (all six depths) ─────────────────────────────────────────
    list_style_names = (
        "List Bullet", "List Bullet 2", "List Bullet 3",
        "List Number", "List Number 2", "List Number 3",
    )
    for style_name in list_style_names:
        try:
            ls = document.styles[style_name]
        except KeyError:
            continue
        ls.font.name = preset.body_font
        ls.font.size = Pt(preset.body_size)
        ls.paragraph_format.space_after = Pt(3)

    # ── Code block ───────────────────────────────────────────────────────────
    if "MDX Code" not in [s.name for s in document.styles]:
        code_style = document.styles.add_style("MDX Code", WD_STYLE_TYPE.PARAGRAPH)
    else:
        code_style = document.styles["MDX Code"]
    code_style.font.name = preset.code_font
    code_style.font.size = Pt(max(9, preset.body_size - 1))
    code_style.paragraph_format.left_indent = Inches(0.3)
    code_style.paragraph_format.right_indent = Inches(0.2)
    code_style.paragraph_format.space_before = Pt(8)
    code_style.paragraph_format.space_after = Pt(10)
    code_style.paragraph_format.line_spacing = 1.0
    _add_code_left_border(code_style, rgb_hex(preset.accent_color))

    return preset


# ── Private helpers ───────────────────────────────────────────────────────────

def _add_code_left_border(style, color_hex: str) -> None:
    """Attach a solid colored left rule to a paragraph style's pPr element."""
    pPr = style.element.get_or_add_pPr()
    # Remove any pre-existing border block to avoid duplicates.
    existing = pPr.find(qn("w:pBdr"))
    if existing is not None:
        pPr.remove(existing)
    pBdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "16")
    left.set(qn("w:space"), "12")
    left.set(qn("w:color"), color_hex)
    pBdr.append(left)
    pPr.append(pBdr)
