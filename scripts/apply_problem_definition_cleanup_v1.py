from __future__ import annotations

from pathlib import Path

TARGET = Path("school/main.tex")
text = TARGET.read_text(encoding="utf-8")
original = text
comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))

old_problem_block = r"""A final disagreement can start at different stages. A dataset reference diagnosis may never enter the candidate list. It may enter the list but fail the criterion check. It may also appear in both the candidate list and the criterion-compatible set, but another diagnosis may still be selected as primary. These cases need different improvements, but one final accuracy score groups them together.

In this thesis, a benchmark or dataset reference label is a diagnosis supplied by the dataset for scoring. It is not an independently reviewed clinical diagnosis. The recorded outputs therefore show where HiED agrees or disagrees with the benchmark; they do not by themselves show which diagnosis is clinically correct.

A high final accuracy score also needs careful interpretation. A text classifier may learn words and label patterns that are common in one corpus. It may score well when its training and test cases come from the same source, but its performance may fall when the data source changes. Same-corpus label prediction, cross-corpus transfer, and the amount of information provided for clinical review are different questions.

The main technical problem studied in this thesis is how to make the three diagnostic decisions separately visible. This allows us to identify whether a benchmark disagreement appears during candidate generation, criterion checking, or primary diagnosis selection. Cross-corpus testing is used as an additional boundary analysis rather than as the main contribution of HiED."""

new_problem_block = r"""A final disagreement can start at different stages. A gold label may never enter the candidate list. It may enter the list but fail the criterion check. It may also appear in both the candidate list and the criterion-compatible set, but another diagnosis may still be selected as primary. These cases need different improvements, but one final accuracy score groups them together.

The main technical problem studied in this thesis is how to make these three diagnostic decisions separately visible. This allows us to identify whether a disagreement appears during candidate generation, criterion checking, or primary diagnosis selection. It also allows different types of disagreement to be studied without treating every final-label mismatch as the same problem."""

single_baseline_paragraph = r"""A Single LLM baseline reads a fixed transcript and directly returns a primary diagnosis. It may also return a comorbid diagnosis. However, it does not follow the same output contract as HiED: it does not provide the same genuine ranked candidate list or an independent criterion-level record for every configured diagnosis. Its output is therefore mainly used to evaluate the final diagnostic result.

"""

if text.count(old_problem_block) != 1:
    raise SystemExit(
        f"Expected the old Section 1.2 block exactly once, found {text.count(old_problem_block)}"
    )
if text.count(single_baseline_paragraph) != 1:
    raise SystemExit(
        "Expected the Single LLM overview paragraph exactly once, "
        f"found {text.count(single_baseline_paragraph)}"
    )

text = text.replace(old_problem_block, new_problem_block, 1)
text = text.replace(single_baseline_paragraph, "", 1)

if comment_counts != (text.count(r"\ct{"), text.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed")

required = [
    r"\section{Problem Definition and Challenges}",
    "A gold label may never enter the candidate list.",
    "The main technical problem studied in this thesis is how to make these three diagnostic decisions separately visible.",
    "It also allows different types of disagreement to be studied without treating every final-label mismatch as the same problem.",
    r"\section{Overview of HiED and Study Scope}",
    "This thesis proposes HiED, a hybrid, evidence-grounded multi-agent decision-support framework for Chinese psychiatric interview transcripts.",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Missing required wording: {missing}")

forbidden = [
    "In this thesis, a benchmark or dataset reference label is a diagnosis supplied by the dataset for scoring.",
    "A high final accuracy score also needs careful interpretation.",
    "Cross-corpus testing is used as an additional boundary analysis rather than as the main contribution of HiED.",
    "A Single LLM baseline reads a fixed transcript and directly returns a primary diagnosis.",
    "it does not provide the same genuine ranked candidate list or an independent criterion-level record for every configured diagnosis",
]
bad = [item for item in forbidden if item in text]
if bad:
    raise SystemExit(f"Stale Introduction wording remains: {bad}")

if text == original:
    raise SystemExit("No change was produced")

TARGET.write_text(text, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Characters: {len(original)} -> {len(text)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")
