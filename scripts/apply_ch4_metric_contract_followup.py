#!/usr/bin/env python3
"""Remove residual statements that overstate TF-IDF Route B coverage."""

from __future__ import annotations

from pathlib import Path

PATH = Path("school/main.tex")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "Training source & 13,000 & Trains conventional baselines and builds the retrieval index; not used for final performance reporting",
        "Route B training source & 13,000 & Required source for leakage-controlled conventional baselines and used to build the retrieval index; no retained TF--IDF Route B run is reported",
        "split-role table",
    )

    text = replace_once(
        text,
        "All internal methods are evaluated on the same fixed 1,000-case held-out set. Because the public-validation split was used during system development, its results are not interpreted as an independent test estimate.",
        "All methods in the main Route B table are reported on the same fixed 1,000-case held-out set. The preserved TF--IDF analysis is explicitly separated because it evaluates the public-validation cases. Because the public-validation split was also used during system development, its results are descriptive development evidence rather than an independent test estimate.",
        "post-split summary",
    )

    text = replace_once(
        text,
        "Internal benchmark positioning (RQ1) & Fixed LingxiDiag internal held-out set, $N=1000$ & Main same-split comparison after configuration selection; complete architectures are compared descriptively",
        "Internal benchmark positioning (RQ1) & Fixed LingxiDiag Route B held-out set, $N=1000$ & Descriptive comparison of Majority, Single, and HiED on Route B; the preserved TF--IDF result is reported separately on public validation",
        "analysis-population table",
    )

    text = replace_once(
        text,
        "The cross-corpus TF--IDF results show that same-source prediction can depend strongly on wording and label priors. The completed evidence therefore supports same-source held-out analysis and a bounded second-synthetic-source test. It does not establish generalization to real psychiatric consultations, independent hospitals, spontaneous or code-switched Taiwanese conversations, or Taiwanese coding practice.",
        "The cross-corpus TF--IDF results show that same-source prediction can depend strongly on wording and label priors. The lexical evidence supports a public-validation same-source sensitivity analysis and a bounded second-synthetic-source transfer test; it is not a Route B held-out estimate. The broader HiED evidence still supports a same-source Route B analysis. Neither line of evidence establishes generalization to real psychiatric consultations, independent hospitals, spontaneous or code-switched Taiwanese conversations, or Taiwanese coding practice.",
        "generalizability boundary",
    )

    text = replace_once(
        text,
        "Most comparisons change more than one component. The main table compares complete TF--IDF, Single, and HiED configurations on the same cases and label mapping, but the methods differ in training, retrieval, prompts, model calls, intermediate outputs, and output contract. Their performance differences cannot be assigned only to multi-agent orchestration.",
        "Most comparisons change more than one component. The Route B table compares Majority, Single, and HiED aggregate configurations under the same intended case universe and label mapping, while the preserved TF--IDF analysis uses the disjoint public-validation population. Single and HiED differ in retrieval, prompts, model calls, intermediate outputs, and output contract, so their performance differences cannot be assigned only to multi-agent orchestration. No direct Route B performance difference between TF--IDF and HiED is estimated.",
        "model-comparison limitation",
    )

    text = replace_once(
        text,
        "Artifact completeness also differs across analyses. The internal HiED headline row, the internal $D_3/I/S$ profiles, the paired DA--NtS comparison, and the matched external trace have case-level support. Several baseline and supporting results remain available only as aggregate summaries or incomplete records. These results cannot support new paired confidence intervals, case-overlap claims, or claims about which individual cases changed.",
        "Artifact completeness also differs across analyses. The internal HiED headline row, the internal $D_3/I/S$ profiles, the paired DA--NtS comparison, and the matched external trace have case-level support. Several baseline and supporting results remain available only as aggregate summaries or incomplete records. The preserved TF--IDF case-level file covers public validation and has zero case-ID overlap with Route B; the legacy TF--IDF aggregate headline row is not reproduced by that file. These results cannot support new paired confidence intervals, same-split case-overlap claims, or claims about which individual cases changed.",
        "artifact-completeness limitation",
    )

    forbidden = [
        "All internal methods are evaluated on the same fixed 1,000-case held-out set",
        "Main same-split comparison after configuration selection",
        "The main table compares complete TF--IDF, Single, and HiED configurations on the same cases",
        "The completed evidence therefore supports same-source held-out analysis",
        "Trains conventional baselines and builds the retrieval index; not used for final performance reporting",
    ]
    remaining = [phrase for phrase in forbidden if phrase in text]
    if remaining:
        raise RuntimeError(f"residual unsupported statements remain: {remaining}")

    PATH.write_text(text, encoding="utf-8")
    print("Applied follow-up split-scope consistency corrections.")


if __name__ == "__main__":
    main()
