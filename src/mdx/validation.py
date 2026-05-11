from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b|\[\s*placeholder\s*\]", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class ValidationIssue:
    severity: str  # "warning" or "error"
    message: str
    line: int | None = None


@dataclass(frozen=True)
class ValidationReport:
    path: Path
    issues: tuple[ValidationIssue, ...]

    @property
    def warnings(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "warning")

    @property
    def errors(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "error")

    @property
    def passed(self) -> bool:
        return self.errors == 0


def validate_markdown_file(
    path: Path,
    *,
    strict: bool = False,
    check_pii: bool = False,
    check_placeholders: bool = True,
    check_tables: bool = True,
    check_headings: bool = True,
    check_links: bool = False,
) -> ValidationReport:
    text = path.read_text(encoding="utf-8")
    issues: list[ValidationIssue] = []
    lines = text.splitlines()

    first_heading_line = None
    first_heading_level = None

    for lineno, line in enumerate(lines, start=1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            if first_heading_line is None:
                first_heading_line = lineno
                first_heading_level = level

    if first_heading_line is None:
        issues.append(ValidationIssue("warning", "Missing title heading (# ...)."))
    elif first_heading_level != 1:
        issues.append(
            ValidationIssue(
                "warning",
                f"First heading should be H1; found H{first_heading_level}.",
                first_heading_line,
            )
        )

    if check_headings:
        _validate_heading_order(lines, issues)

    if check_placeholders:
        _validate_placeholders(lines, issues)

    if check_pii:
        _validate_pii(lines, issues)

    if check_tables:
        _validate_tables(lines, issues)

    if check_links:
        _validate_local_links(path, lines, issues)

    if "```mermaid" in text:
        issues.append(
            ValidationIssue(
                "warning",
                "Mermaid block detected; diagrams may require separate rendering for DOCX output.",
            )
        )

    if strict:
        strict_promotions = [
            ValidationIssue("error", issue.message, issue.line)
            if issue.severity == "warning"
            else issue
            for issue in issues
        ]
        return ValidationReport(path=path, issues=tuple(strict_promotions))

    return ValidationReport(path=path, issues=tuple(issues))


def summarize_reports(reports: Iterable[ValidationReport]) -> tuple[int, int]:
    warnings = 0
    errors = 0
    for report in reports:
        warnings += report.warnings
        errors += report.errors
    return warnings, errors


def _validate_heading_order(lines: list[str], issues: list[ValidationIssue]) -> None:
    previous_level = 0
    for lineno, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        if previous_level and level > previous_level + 1:
            issues.append(
                ValidationIssue(
                    "warning",
                    f"Heading jumps from H{previous_level} to H{level}.",
                    lineno,
                )
            )
        previous_level = level


def _validate_placeholders(lines: list[str], issues: list[ValidationIssue]) -> None:
    for lineno, line in enumerate(lines, start=1):
        if PLACEHOLDER_RE.search(line):
            issues.append(
                ValidationIssue(
                    "warning",
                    f'Placeholder text detected: "{line.strip()}".',
                    lineno,
                )
            )


def _validate_pii(lines: list[str], issues: list[ValidationIssue]) -> None:
    for lineno, line in enumerate(lines, start=1):
        if EMAIL_RE.search(line):
            issues.append(ValidationIssue("warning", "Possible email address detected.", lineno))
        if PHONE_RE.search(line):
            issues.append(ValidationIssue("warning", "Possible phone number detected.", lineno))


def _validate_tables(lines: list[str], issues: list[ValidationIssue]) -> None:
    for lineno, line in enumerate(lines, start=1):
        if "|" not in line:
            continue
        parts = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(parts) > 1 and any(cell == "" for cell in parts):
            issues.append(ValidationIssue("warning", "Table row contains empty cells.", lineno))


def _validate_local_links(path: Path, lines: list[str], issues: list[ValidationIssue]) -> None:
    for lineno, line in enumerate(lines, start=1):
        for target in LINK_RE.findall(line):
            target = target.strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                issues.append(
                    ValidationIssue(
                        "warning",
                        f"Broken local link target: {target}",
                        lineno,
                    )
                )
