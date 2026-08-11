from __future__ import annotations

from pathlib import Path
import re

TARGET = Path("school/main.tex")
FRAGMENT = Path("scripts/ch2_rewrite_v2/chapter2.tex")

text = TARGET.read_text(encoding="utf-8")
new_chapter = FRAGMENT.read_text(encoding="utf-8").strip()
original = text
comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))

start_marker = r"\chapter{Related Work}"
end_marker = r"\chapter{Study Architectures and Diagnostic Workflow}"
start = text.index(start_marker)
end = text.index(end_marker, start)
old_chapter = text[start:end]


def citation_keys(block: str) -> set[str]:
    keys: set[str] = set()
    for match in re.finditer(r"\\cite[pt]?\{([^}]+)\}", block):
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


old_keys = citation_keys(old_chapter)
new_keys = citation_keys(new_chapter)
if old_keys != new_keys:
    raise SystemExit(
        "Chapter 2 citation-key set changed: "
        f"removed={sorted(old_keys - new_keys)}, added={sorted(new_keys - old_keys)}"
    )

if r"\ct{" in old_chapter or r"\wl{" in old_chapter:
    raise SystemExit("Advisor comments found inside Chapter 2; refusing replacement")

text = text[:start] + new_chapter + "\n\n" + text[end:]

if comment_counts != (text.count(r"\ct{"), text.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed")

required = [
    r"\chapter{Related Work}",
    r"\section{Psychiatric LLM Diagnosis}",
    r"\section{Decision Support, Auditability, and Criterion-Level Records}",
    r"\label{sec:auditability-definition}",
    r"\section{Primary Diagnosis Selection}",
    r"\section{Retrieval with Similar Cases}",
    r"\section{Medical Multi-Agent Systems}",
    r"\section{Research Gap and Research Questions}",
    r"\label{tab:related-work-matrix}",
    "The main gap is not the absence of another final-label predictor.",
    "This thesis addresses the main gap through the stage-wise analysis in RQ2.",
    "RQ2 is the main stage-wise analysis.",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Missing required Chapter 2 wording: {missing}")

new_block = text[start:text.index(end_marker, start)]
forbidden = [
    "benchmark-reference diagnosis",
    "benchmark-reference inclusion",
    "This thesis uses example retrieval.",
    "Most published studies still focus on the final diagnosis.",
    "The reviewed work leaves five questions that are directly related to this thesis:",
]
bad = [item for item in forbidden if item in new_block]
if bad:
    raise SystemExit(f"Stale Chapter 2 wording remains: {bad}")

if text == original:
    raise SystemExit("Rewrite produced no change")

TARGET.write_text(text, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Chapter 2 citation keys preserved: {len(new_keys)}")
print(f"Characters: {len(original)} -> {len(text)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")
