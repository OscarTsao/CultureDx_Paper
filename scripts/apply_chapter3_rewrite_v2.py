from __future__ import annotations

from pathlib import Path
import re


TARGET = Path("school/main.tex")
TEMPLATE = Path("scripts/ch3_rewrite_v2/chapter3_template.tex")

text = TARGET.read_text(encoding="utf-8")
original = text
comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))

chapter_start_marker = r"\chapter{Study Architectures and Diagnostic Workflow}"
chapter_end_marker = r"\chapter{Datasets, Label Projection, and Evaluation Protocol}"

if chapter_start_marker not in text:
    raise SystemExit("Could not find the existing Chapter 3 start marker")
if chapter_end_marker not in text:
    raise SystemExit("Could not find the Chapter 4 start marker")

chapter_start = text.index(chapter_start_marker)
chapter_end = text.index(chapter_end_marker, chapter_start)
old_chapter = text[chapter_start:chapter_end]

transcript_marker = r"\subsection{Complete Constructed Transcript}"
single_marker = r"\subsection{Illustrative Single LLM Output}"
hied_marker = r"\subsection{Illustrative HiED Outputs}"
what_marker = r"\subsection{What the Example Demonstrates}"
summary_marker = r"\section{Chapter Summary}"

for marker in [transcript_marker, single_marker, hied_marker, what_marker, summary_marker]:
    if marker not in old_chapter:
        raise SystemExit(f"Missing Chapter 3 extraction marker: {marker}")

transcript_start = old_chapter.index(transcript_marker)
single_start = old_chapter.index(single_marker, transcript_start)
hied_start = old_chapter.index(hied_marker, single_start)
what_start = old_chapter.index(what_marker, hied_start)
summary_start = old_chapter.index(summary_marker, what_start)

transcript_block = old_chapter[transcript_start:single_start].strip()
single_block = old_chapter[single_start:hied_start].strip()
hied_block = old_chapter[hied_start:what_start].strip()
what_block = old_chapter[what_start:summary_start].strip()

# Move the worked-example overview figure before the complete transcript.
figure_intro = r"Figure~\ref{fig:worked-example-flow} summarizes these recorded outputs."
if figure_intro not in hied_block:
    raise SystemExit("Could not find the existing worked-example figure block")
figure_start = hied_block.index(figure_intro)
float_barrier = r"\FloatBarrier"
figure_end = hied_block.index(float_barrier, figure_start) + len(float_barrier)
hied_block = (hied_block[:figure_start] + hied_block[figure_end:]).strip()

# Give the remaining worked-example material a clearer stage-wise structure.
hied_block = hied_block.replace(
    r"\subsection{Illustrative HiED Outputs}",
    r"\subsection{Diagnosis-Path Outputs}",
    1,
)
criterion_intro = r"Table~\ref{tab:worked-example-criteria} presents selected criterion states for three diagnoses."
if criterion_intro not in hied_block:
    raise SystemExit("Could not find the criterion-state example marker")
hied_block = hied_block.replace(
    criterion_intro,
    r"\subsection{Criterion States and Missing Information}" + "\n\n" + criterion_intro,
    1,
)
final_table_marker = "\\begin{table}[htbp]\n\\centering\n\\caption{Illustrative compatibility and finalization outputs.}"
if final_table_marker not in hied_block:
    raise SystemExit("Could not find the finalization example table")
hied_block = hied_block.replace(
    final_table_marker,
    r"\subsection{DA and NtS Selection Results}" + "\n\n" + final_table_marker,
    1,
)

new_chapter = TEMPLATE.read_text(encoding="utf-8").strip()
replacements = {
    "@@TRANSCRIPT_BLOCK@@": transcript_block,
    "@@SINGLE_BLOCK@@": single_block,
    "@@HIED_BLOCK@@": hied_block,
    "@@WHAT_BLOCK@@": what_block,
}
for placeholder, value in replacements.items():
    if new_chapter.count(placeholder) != 1:
        raise SystemExit(f"Template placeholder count is not one: {placeholder}")
    new_chapter = new_chapter.replace(placeholder, value)

text = text[:chapter_start] + new_chapter + "\n\n" + text[chapter_end:]

if comment_counts != (text.count(r"\ct{"), text.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed")

required = [
    r"\chapter{HiED Architecture and Stage-Wise Diagnostic Workflow}",
    r"\section{Task Input, Diagnostic Scope, and Recorded Outputs}",
    r"\label{tab:configured-profile-summary}",
    r"\label{tab:hied-output-space}",
    r"\includegraphics[width=1.0\textwidth]{fig_hied_two_path_architecture.pdf}",
    r"\section{Single LLM Baseline and Comparison Contract}",
    r"\subsection{Complete Constructed Transcript}",
    r"\subsection{Criterion States and Missing Information}",
    r"\subsection{DA and NtS Selection Results}",
    r"\section{Chapter Summary}",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Missing required Chapter 3 anchors: {missing}")

forbidden = [
    r"\chapter{Study Architectures and Diagnostic Workflow}",
    "The study evaluates three retrieval conditions: no retrieval, global Top-5 retrieval, and parent-balanced retrieval.",
    r"\includegraphics[width=1.0\textwidth]{fig_single_vs_hied_architecture.pdf}",
    r"\subsection{Diagnostic Output Roles}",
]
bad = [item for item in forbidden if item in text]
if bad:
    raise SystemExit(f"Stale Chapter 3 wording remains: {bad}")

# Check literal labels for accidental duplication. Figure aliases are intentional
# but still use distinct label names.
labels = re.findall(r"\\label\{([^}]+)\}", text)
duplicates = sorted({label for label in labels if labels.count(label) > 1})
if duplicates:
    raise SystemExit(f"Duplicate labels after Chapter 3 rewrite: {duplicates}")

if text == original:
    raise SystemExit("Chapter 3 rewrite produced no changes")

TARGET.write_text(text, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Characters: {len(original)} -> {len(text)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")
