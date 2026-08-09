from __future__ import annotations

from pathlib import Path
import re
import sys

TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("school/main.tex")
FRAGMENT = Path(__file__).resolve().parent / "ch2_plain_v1" / "chapter2.tex"

text = TARGET.read_text(encoding="utf-8")
replacement = FRAGMENT.read_text(encoding="utf-8").strip()
start_marker = r"\chapter{Related Work}"
end_marker = r"\chapter{Study Architectures and Diagnostic Workflow}"

if text.count(start_marker) != 1 or text.count(end_marker) != 1:
    raise SystemExit("Could not locate the Chapter 2 replacement boundaries exactly once.")

start = text.index(start_marker)
end = text.index(end_marker, start)
old = text[start:end]

if r"\ct{" in old or r"\wl{" in old:
    raise SystemExit("Advisor comments were found inside Chapter 2; refusing automatic replacement.")

old_cites = set()
for match in re.finditer(r"\\cite[pt]?\{([^}]+)\}", old):
    old_cites.update(key.strip() for key in match.group(1).split(",") if key.strip())
new_cites = set()
for match in re.finditer(r"\\cite[pt]?\{([^}]+)\}", replacement):
    new_cites.update(key.strip() for key in match.group(1).split(",") if key.strip())
if old_cites != new_cites:
    raise SystemExit(
        f"Chapter 2 citation-key set changed. Removed={sorted(old_cites-new_cites)} Added={sorted(new_cites-old_cites)}"
    )

comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))
updated = text[:start] + replacement + "\n\n" + text[end:]
if comment_counts != (updated.count(r"\ct{"), updated.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed.")

required = [
    r"\chapter{Related Work}",
    r"\label{ch:related}",
    r"\section{Psychiatric LLM Diagnosis}",
    r"\section{Retrieval with Similar Cases}",
    r"\section{Medical Multi-Agent Systems}",
    r"\section{Auditability and Criterion-Level Records}",
    r"\label{sec:auditability-definition}",
    r"\section{Primary Diagnosis Selection}",
    r"\section{Research Gap and Research Questions}",
    r"\label{tab:related-work-matrix}",
    r"\item[RQ1] How does HiED perform relative to conventional classification and a Single LLM on the same internal split and parent-label evaluation?",
    r"\item[RQ5] Does the stage-wise analysis remain useful under a second synthetic source?",
]
missing = [item for item in required if item not in replacement]
if missing:
    raise SystemExit(f"Missing required Chapter 2 anchors: {missing}")

forbidden = [
    "criterion-grounded audit records",
    "fine-grained differential diagnosis",
    "indexed corpus",
    "This creates an attribution problem",
    "heterogeneous knowledge graphs",
    "explanatory dependence",
]
bad = [item for item in forbidden if item in replacement]
if bad:
    raise SystemExit(f"Old difficult wording remains in Chapter 2: {bad}")

# Protect global labels and references, including labels created by \ThesisFigure.
literal_labels = re.findall(r"\\label\{([^}]+)\}", updated)
macro_labels = re.findall(
    r"\\ThesisFigure(?:\[[^\]]*\])?\{[^\n]*\}\{[^\n]*\}\{([^}]+)\}", updated
)
labels = literal_labels + macro_labels
refs: list[str] = []
for pattern in [
    r"\\ref\{([^}]+)\}",
    r"\\cref\{([^}]+)\}",
    r"\\Cref\{([^}]+)\}",
    r"\\pageref\{([^}]+)\}",
]:
    refs.extend(re.findall(pattern, updated))
missing_refs = sorted(set(refs) - set(labels))
duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
if missing_refs or duplicate_labels:
    raise SystemExit(f"missing references={missing_refs}; duplicate labels={duplicate_labels}")

TARGET.write_text(updated, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Chapter 2 characters: {len(old)} -> {len(replacement)}")
print(f"Citation keys preserved: {len(old_cites)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")
