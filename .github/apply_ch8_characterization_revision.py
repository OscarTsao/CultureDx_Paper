from __future__ import annotations

import re
import sys
from pathlib import Path


def sub_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(
        pattern, lambda _match: replacement, text, count=1, flags=re.DOTALL
    )
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return updated


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_ch8_characterization_revision.py TARGET_TEX")

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    examples_match = re.search(
        r"\\section\{Selected Frozen-Output Examples\}\n"
        r"\\label\{sec:ch8-trace-boundaries\}\n.*?"
        r"(?=\\section\{Chapter Summary\})",
        text,
        flags=re.DOTALL,
    )
    if examples_match is None:
        raise RuntimeError("frozen examples: expected one section")
    examples_block = examples_match.group(0).rstrip() + "\n\n"
    main_examples_pointer = r"""\paragraph{Frozen-record examples.}
Deterministically selected examples from four recorded-output profiles are provided in Appendix~\ref{app:supporting}, Table~\ref{tab:audit-trace-examples}. These examples document how the indicators map to individual frozen records without treating them as representative clinical cases.

"""
    text = (
        text[: examples_match.start()]
        + main_examples_pointer
        + text[examples_match.end() :]
    )

    chapter_opening = r"""\chapter{Characterization of Recorded-Output Disagreements}
\label{ch:error}

This chapter characterizes the disagreements identified in Chapter~\ref{ch:results}. It does not repeat the internal performance comparison or estimate clinical diagnostic error. LingxiDiag contains synthetic dialogues, the benchmark labels are dataset references rather than independently adjudicated clinical diagnoses, and the saved outputs do not reveal the model's hidden reasoning.

\section{Analysis Scope}
\label{sec:ch8-stagewise-taxonomy}

Chapter~\ref{ch:results} divided the 915 checker-eligible cases into mutually exclusive groups using genuine Top-3 detection ($D_3$), benchmark-gold inclusion in the criterion-compatible set ($I$), and committed-primary agreement ($S$). This chapter focuses on characteristics that are not visible from the aggregate group counts: the rank of the benchmark-reference diagnosis, frequent reference-to-primary directions, disagreement in the complete emitted diagnosis set, and the composition of recorded criterion states.

Particular attention is given to the 272 cases with $D_3=1$, $I=1$, and $S=0$. In these cases, a benchmark-reference diagnosis is present in both the genuine Top-3 and the criterion-compatible set, but no benchmark-reference parent is committed as the primary diagnosis. $S=0$ does not imply that every benchmark-reference diagnosis is absent from the optional comorbid output. The analysis therefore describes a primary-commitment disagreement rather than the complete removal of the reference diagnosis.

The analysis uses one frozen 1,000-case internal held-out trace. The 349-case gold-informed oracle population reported in Chapter~\ref{ch:results} is not an observed system group and is not used here.

"""
    text = sub_once(
        text,
        r"\\chapter\{Characterization of Recorded-Output Disagreements\}\n"
        r"\\label\{ch:error\}\n.*?"
        r"(?=\\section\{Ranked and Criterion-Compatible but Not Selected\})",
        chapter_opening,
        "chapter opening and repeated profile recap",
    )

    text = replace_once(
        text,
        r"\section{Ranked and Criterion-Compatible but Not Selected}",
        r"\section{Rank and Diagnostic Direction within the Primary-Commitment Disagreement Group}",
        "rank section title",
    )
    text = replace_once(
        text,
        "The 272-case group is examined in more detail because it is the largest recorded benchmark-disagreement profile. Figure~\\ref{fig:ch8-reference-rank} shows the position of the highest-ranked benchmark-reference parent.",
        "The 272-case group is examined in more detail because it is the largest mutually exclusive disagreement group among the checker-eligible cases. Figure~\\ref{fig:ch8-reference-rank} shows the position of the highest-ranked benchmark-reference parent.",
        "rank section opening",
    )
    text = replace_once(
        text,
        r"\ThesisFigure[0.72\textwidth]{fig_ch8_reference_rank.pdf}{Rank of the highest-ranked benchmark-reference parent among the 272 cases with $D_3=1$, $I=1$, and $S=0$.}{fig:ch8-reference-rank}",
        r"\ThesisFigure[0.72\textwidth]{fig_ch8_reference_rank.pdf}{Rank of the highest-ranked benchmark-reference parent among the 272 cases with $D_3=1$, $I=1$, and $S=0$, in which no benchmark-reference parent is committed as primary.}{fig:ch8-reference-rank}",
        "rank figure caption",
    )
    text = replace_once(
        text,
        "The benchmark-reference parent is ranked second in 171 cases (62.9\\%) and third in 101 cases (37.1\\%). In most cases it is therefore the closest recorded alternative to the leading diagnosis, but rank proximity alone does not explain why another diagnosis is committed.",
        "The benchmark-reference parent is ranked second in 171 cases (62.9\\%) and third in 101 cases (37.1\\%). In this group, the reference can only occupy rank two or three because another diagnosis is committed as primary and the reference is required to appear in the Top-3. The result therefore shows that the reference is more often the immediate alternative at rank two than a rank-three candidate; it does not explain why the primary commitment differs.",
        "rank interpretation",
    )
    text = replace_once(
        text,
        r"\caption{Most frequent benchmark-reference-to-committed-primary pairs in the 272-case group.}",
        r"\caption{Most frequent benchmark-reference-to-committed-primary directions in the 272-case primary-commitment disagreement group.}",
        "pair table caption",
    )
    text = replace_once(
        text,
        r"\textit{Note.} Each case contributes one pair based on its highest-ranked benchmark-reference parent. Percentages use the 272-case group as the denominator; only the five most frequent pairs are shown.}",
        r"\textit{Note.} Each case contributes one pair based on its highest-ranked benchmark-reference parent. Percentages use the 272-case group as the denominator; only the five most frequent pairs are shown. These raw counts are not normalized by class prevalence and therefore describe frequent directions rather than class-specific error rates.}",
        "pair table note",
    )

    text = replace_once(
        text,
        r"\section{Diagnostic-Set Construction Disagreements}",
        r"\section{Diagnostic-Set Disagreement after Primary Agreement}",
        "diagnostic-set section title",
    )
    text = replace_once(
        text,
        "Committed-primary agreement does not guarantee agreement between the complete emitted diagnosis set and the benchmark-reference set. Among the 1,000 internal cases, HiED--DA commits a benchmark-consistent primary diagnosis in 518 cases. Exact set agreement occurs in 409 cases, leaving 109 cases with primary agreement but diagnostic-set disagreement.",
        "Committed-primary agreement does not guarantee agreement between the complete emitted diagnosis set and the benchmark-reference set. Among the 1,000 internal cases, HiED--DA commits a benchmark-consistent primary diagnosis in 518 cases. Exact set agreement occurs in 409 cases, leaving 109 cases (21.0\\% of the 518 primary-agreement cases) with primary agreement but diagnostic-set disagreement. Primary agreement therefore does not imply agreement on comorbidity or additional diagnostic labels.",
        "diagnostic-set interpretation",
    )

    text = replace_once(
        text,
        "The Criterion Checker records each item as \\texttt{met}, \\texttt{not\\_met}, or \\texttt{insufficient\\_\\allowbreak{}evidence}. Figure~\\ref{fig:ch8-criterion-composition} compares mean within-case proportions across the four mutually exclusive analysis groups. Each case is summarized before group averaging so that cases with more recorded criterion items do not receive more weight. The corresponding medians and interquartile ranges are reported in Appendix~\\ref{app:supporting}, Table~\\ref{tab:ch8-criterion-ratios}.",
        "The Criterion Checker records each item as \\texttt{met}, \\texttt{not\\_met}, or \\texttt{insufficient\\_\\allowbreak{}evidence}. Figure~\\ref{fig:ch8-criterion-composition} compares mean within-case proportions across the four mutually exclusive analysis groups. For each case, the states are aggregated across all fourteen configured Criterion Checkers; the frozen trace contains 77,998 diagnosis-by-criterion states. Each case is summarized before group averaging so that cases with more recorded criterion items do not receive more weight. The corresponding medians and interquartile ranges are reported in Appendix~\\ref{app:supporting}, Table~\\ref{tab:ch8-criterion-ratios}.",
        "criterion composition analysis unit",
    )
    text = replace_once(
        text,
        "The 272-case group and the committed-primary-agreement group have closely overlapping criterion-state compositions. Top-3 candidate misses are also broadly similar. The 12-case ranked-but-not-compatible disagreement group has fewer \\texttt{met} states and more unresolved evidence on average, but its small size does not support a stable group-level conclusion.\n\nCriterion checking makes the problem easier to inspect, but broad compatibility does not solve the final comparison. Compatible-set size and aggregate criterion-state proportions do not identify which compatible diagnosis will be committed as primary in this trace. These summaries are descriptive associations, not evidence that one criterion-state pattern caused the final commitment.",
        "At this coarse aggregate level, no clear separation is visible between the committed-primary-agreement group and the 272-case primary-commitment disagreement group. Their mean proportions of \\texttt{met}, \\texttt{not\\_met}, and \\texttt{insufficient\\_\\allowbreak{}evidence} states are similar. Top-3 candidate misses are also broadly similar. The 12-case ranked-but-not-compatible disagreement group has fewer \\texttt{met} states and more unresolved evidence on average, but its small size does not support a stable group-level conclusion.\n\nBecause this analysis aggregates criterion states across all fourteen configured diagnoses, it may conceal diagnosis-specific or candidate-pair-specific differences. The result shows the limitation of a global state-composition summary; it does not show that criterion-level evidence is uninformative. Compatible-set size and aggregate criterion-state proportions do not identify which compatible diagnosis will be committed as primary in this trace, and these summaries do not establish that one state pattern caused the final commitment.",
        "criterion composition interpretation",
    )

    revised_summary = r"""\section{Chapter Summary}
\label{sec:ch8-summary}

The detailed analysis adds four findings to the stage-wise results reported in Chapter~\ref{ch:results}. First, among the 272 cases in which a benchmark-reference diagnosis is ranked and criterion-compatible but no benchmark-reference parent is committed as primary, the reference is more often ranked second than third. Second, the disagreement directions are concentrated, especially from F41 to F32, although these raw counts are influenced by class prevalence and are not class-specific error rates. Third, committed-primary agreement does not guarantee complete-set agreement: 109 of 518 primary-agreement cases (21.0\%) still differ from the benchmark diagnosis set. Fourth, the aggregate composition of criterion states is similar between the primary-agreement group and the largest primary-commitment disagreement group, indicating that global proportions of \texttt{met}, \texttt{not\_met}, and \texttt{insufficient\_\allowbreak{}evidence} states do not by themselves explain the final commitment.

These findings characterize the recorded outputs but do not identify clinically adjudicated errors, establish a universal finalization bottleneck, or prove a causal effect of criterion states. Diagnosis-specific comparisons and clinician review are needed to determine whether the observed benchmark disagreements reflect system error, missing transcript information, or ambiguity in the reference labels.

"""
    text = sub_once(
        text,
        r"\\section\{Chapter Summary\}\n"
        r"\\label\{sec:ch8-summary\}\n.*?"
        r"(?=\\chapter\{Discussion\})",
        revised_summary,
        "chapter summary",
    )

    text = replace_once(
        text,
        "Ranked and compatible, not selected",
        "Ranked and compatible, not primary",
        "appendix criterion-ratio group label",
    )

    appendix_marker = r"\section{Auxiliary Primary-Selection Configurations}"
    text = replace_once(
        text,
        appendix_marker,
        examples_block + appendix_marker,
        "move frozen examples to appendix",
    )

    path.write_text(text, encoding="utf-8")
    print(f"Applied Chapter 8 characterization revision to {path}")


if __name__ == "__main__":
    main()
