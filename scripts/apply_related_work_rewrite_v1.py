from __future__ import annotations

from pathlib import Path
import re
import sys

TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("school/main.tex")
CHAPTER = (
    Path(__file__).resolve().parent / "related_work_v1" / "chapter2.tex"
).read_text(encoding="utf-8").strip()

text = TARGET.read_text(encoding="utf-8")
original = text
comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))

start_marker = r"\chapter{Related Work}"
end_marker = r"\chapter{Study Architectures and Diagnostic Workflow}"
if text.count(start_marker) != 1 or text.count(end_marker) != 1:
    raise SystemExit("Chapter 2 boundary markers were not found exactly once")

start = text.index(start_marker)
end = text.index(end_marker, start)
old_chapter = text[start:end]
if r"\ct{" in old_chapter or r"\wl{" in old_chapter:
    raise SystemExit("Advisor comments were found inside Chapter 2; refusing replacement")

updated = text[:start] + CHAPTER + "\n\n" + text[end:]

if comment_counts != (updated.count(r"\ct{"), updated.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed")

# Global label/reference integrity, including labels stored as the fourth ThesisFigure argument.
literal_labels = re.findall(r"\\label\{([^}]+)\}", updated)
macro_labels = re.findall(
    r"\\ThesisFigure(?:\[[^\]]*\])?\{[^\n]*\}\{[^\n]*\}\{([^}]+)\}",
    updated,
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
    raise SystemExit(
        f"missing references={missing_refs}; duplicate labels={duplicate_labels}"
    )

required = [
    r"\chapter{Related Work}",
    r"\label{ch:related}",
    r"\section{Psychiatric LLM Diagnosis}",
    r"\section{Retrieval-Augmented Diagnostic Reasoning}",
    r"\section{Medical Multi-Agent Reasoning}",
    r"\section{Auditability and Criterion Grounding}",
    r"\label{sec:auditability-definition}",
    r"\section{Primary-Diagnosis Selection}",
    r"\section{Research Gap and Research Questions}",
    r"\label{tab:related-work-matrix}",
    "How does HiED perform relative to conventional classification and a Single LLM",
    "Where is benchmark disagreement recorded across candidate generation, criterion checking, compatibility analysis, and primary commitment?",
    "Does the stage-wise analysis remain useful under a second synthetic source?",
    "These are possible benefits, not guarantees.",
    "Retrieved cases are examples from the training source, not medical evidence about the current patient.",
]
missing = [item for item in required if item not in updated]
if missing:
    raise SystemExit(f"Missing required Chapter 2 anchors: {missing}")

chapter_end = updated.index(end_marker, start)
new_chapter = updated[start:chapter_end]
for forbidden in [
    "allowing performance changes to be attributed to specific functions",
    "diagnostic-scope, cross-corpus transfer, and error-pattern analyses",
    "criterion verification",
    "an increase in the number of agents or interaction rounds does not by itself establish better diagnostic accuracy",
]:
    if forbidden in new_chapter:
        raise SystemExit(f"Old dense wording remains in Chapter 2: {forbidden}")

# Preserve the cited literature set used by the reviewed Chapter 2 source.
required_citations = [
    "qiu2023largeai",
    "xu2026lingxidiagbench",
    "yin2024mdd5k",
    "li2026mind",
    "wu2026wisemind",
    "bi2025magi",
    "ozgun2025dsm5agentflow",
    "sun2026mentalseek",
    "xiao2025moodangels",
    "lewis2020rag",
    "liu2022incontext",
    "tang2024medagents",
    "kim2024mdagents",
    "du2024debate",
    "turpin2023unfaithful",
    "rudin2019stop",
    "huang2024xiai",
    "kim2025clp",
    "wang2025medkgi",
    "ge2024dkec",
]
missing_citations = [key for key in required_citations if key not in new_chapter]
if missing_citations:
    raise SystemExit(f"Required source citations were lost: {missing_citations}")

if updated == original:
    raise SystemExit("Rewrite produced no changes")

TARGET.write_text(updated, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Old Chapter 2 chars: {len(old_chapter)}")
print(f"New Chapter 2 chars: {len(CHAPTER)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")
