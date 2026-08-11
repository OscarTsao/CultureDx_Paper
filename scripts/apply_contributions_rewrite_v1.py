from __future__ import annotations

from pathlib import Path

TARGET = Path("school/main.tex")
text = TARGET.read_text(encoding="utf-8")
original = text
comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))

old = r"""\section{Contributions}

This thesis makes two main contributions.

First, it presents a two-path and stage-wise architecture for psychiatric decision support. Compared with a Single LLM that mainly returns a final diagnostic output, HiED separately records the ranked candidate list, criterion-checking results, criterion-compatible set, and committed primary diagnosis. This design allows candidate generation, criterion checking, and primary diagnosis selection to be studied separately. Using these outputs, this thesis finds that primary commitment contains the largest recorded benchmark-disagreement profile in the two tested synthetic datasets. This is a benchmark finding under the evaluated settings, not a claim about the true clinical primary diagnosis in every case.

Second, HiED provides structured diagnostic information for clinical review instead of only one final diagnosis. It returns ranked possible diagnoses and marks each diagnostic criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. It also keeps the criterion-compatible set and the final selection record. These outputs are designed to help clinicians screen possible diagnoses, review supporting or conflicting evidence, and identify what information is still missing. Their effect on clinical speed, accuracy, and safety still requires direct clinical evaluation."""

new = r"""\section{Contributions}

This thesis makes two main contributions.

First, it proposes a stage-wise architecture for psychiatric decision support. HiED separates candidate generation, criterion checking, and primary-diagnosis selection, and keeps the output of each stage. This makes it possible to identify where a diagnostic disagreement appears instead of treating every wrong final label as the same problem. Using this analysis, we found that the largest disagreement group in both datasets appeared at primary-diagnosis selection. In 272 LingxiDiag-16K cases and 225 MDD-5k cases, at least one gold label was already in the Top-3 and the criterion-compatible set, but the system selected another primary diagnosis.

Second, it provides structured information for clinical review instead of only a final diagnosis. HiED returns a ranked candidate list and marks each diagnostic criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. It also records the criterion-compatible set and the information that is still missing. These outputs are designed to help clinicians quickly screen possible diagnoses, locate the symptoms and criterion evidence relevant to each candidate, and identify what information should be collected next.

Together, these contributions shift the focus from only predicting a final label to supporting stage-wise analysis and clinical review."""

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected the old Contributions block exactly once, found {count}")

text = text.replace(old, new, 1)

if comment_counts != (text.count(r"\ct{"), text.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed")

required = [
    "First, it proposes a stage-wise architecture for psychiatric decision support.",
    "In 272 LingxiDiag-16K cases and 225 MDD-5k cases, at least one gold label was already in the Top-3 and the criterion-compatible set, but the system selected another primary diagnosis.",
    "Second, it provides structured information for clinical review instead of only a final diagnosis.",
    "Together, these contributions shift the focus from only predicting a final label to supporting stage-wise analysis and clinical review.",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Missing required Contributions wording: {missing}")

forbidden = [
    "Compared with a Single LLM that mainly returns a final diagnostic output",
    "This is a benchmark finding under the evaluated settings",
    "Their effect on clinical speed, accuracy, and safety still requires direct clinical evaluation.",
]
bad = [item for item in forbidden if item in text]
if bad:
    raise SystemExit(f"Stale Contributions wording remains: {bad}")

if text == original:
    raise SystemExit("No change was produced")

TARGET.write_text(text, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Characters: {len(original)} -> {len(text)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")
