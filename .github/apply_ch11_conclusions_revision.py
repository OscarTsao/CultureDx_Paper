from __future__ import annotations

import sys
from pathlib import Path


NEW_CHAPTER = r'''\chapter{Conclusions and Future Work}
\label{ch:conclusion}

\section{Summary of Findings}

This thesis presented HiED, a stage-wise decision-support framework for Chinese psychiatric interview transcripts. HiED retains candidate generation, criterion checking, compatibility analysis, and primary commitment as separate recorded output views. It provides ranked candidates, criterion states, a criterion-compatible set, missing-information records, and the final commitment source.

On the fixed internal held-out set, TF--IDF with logistic regression provides the strongest same-source primary-label and class-level F1 performance, while Single and HiED have almost identical committed Top-1 results. The separate cross-corpus analysis shows that the lexical advantage of TF--IDF with logistic regression is strongly source-sensitive and should not be interpreted as source-independent diagnostic performance. HiED therefore does not establish an overall final-label accuracy advantage.

HiED's completed technical contribution is a same-case stage-wise output and evaluation contract. Ranked candidates, criterion states, the criterion-compatible set, and the committed primary diagnosis are retained for the same cases and evaluated separately. This makes it possible to distinguish candidate absence, compatibility disagreement, and primary-commitment disagreement without claiming access to hidden model reasoning.

The largest internal benchmark-disagreement profile contains 272 of 915 checker-eligible cases. In these cases, a benchmark-reference diagnosis is present in both the genuine Top-3 and the criterion-compatible set, but no benchmark-reference parent is committed as primary. A corresponding profile contains 225 of 878 checker-eligible cases in the matched MDD-5k trace. The repeated profile supports the portability of the stage-wise analysis questions across two synthetic sources, but the numerical rates are not stable across corpora or archived trace lineages.

None of the tested primary-selection methods provides a clear and attributable improvement over Direct-Answer. In particular, Nominate-then-Select lowers committed Top-1 under all three internal retrieval conditions. The experiments show that candidate availability and criterion compatibility create decision headroom, but do not provide a simple or automatically recoverable rule for primary commitment.

The structured outputs are intended to support review by showing possible diagnoses, criterion states, and missing information. Their effect on clinical accuracy, speed, safety, workflow, or patient outcomes has not been demonstrated. HiED should therefore be interpreted as an offline research and review framework rather than a clinically validated diagnostic system.

\section{Answers to the Research Questions}

The answers below apply only to the tested synthetic datasets, label mappings, output contracts, and preserved result traces.

\begin{description}[style=nextline,leftmargin=1.5cm,labelwidth=1.1cm,itemsep=0.2em,parsep=0pt]

\item[RQ1] \textbf{How does HiED perform relative to conventional classification and a Single LLM on the same internal split and parent-label evaluation?}

TF--IDF with logistic regression provides the strongest same-source primary-label and class-level F1 performance. Single and HiED have almost identical committed Top-1 values. HiED does not establish an overall internal accuracy advantage, but it provides a genuine ranked differential, criterion states, a criterion-compatible set, and a final commitment record for stage-wise analysis. The separate cross-corpus analysis shows that the lexical advantage of TF--IDF with logistic regression is source-sensitive rather than source-independent.

\item[RQ2] \textbf{Where is benchmark disagreement recorded across candidate generation, criterion checking, compatibility analysis, and primary commitment?}

The largest internal disagreement profile contains 272 checker-eligible cases in which a benchmark-reference diagnosis is present in both the genuine Top-3 and the criterion-compatible set but no benchmark-reference parent is committed as primary. This is the largest recorded primary-commitment disagreement profile under the tested HiED configuration. It is not proof of a universal clinical bottleneck or a causal failure of the finalizer alone.

\item[RQ3] \textbf{How do similar-case retrieval strategies affect Single and HiED?}

Retrieval produces consistently higher Top-1 point estimates for Single than no retrieval. For HiED, the differences among no retrieval, global Top-5 retrieval, and parent-balanced retrieval are smaller and depend on the split and metric. Parent-balanced retrieval is retained by the predefined validation procedure, while global Top-5 has higher post-selection held-out point estimates. The study does not establish one retrieval policy as universally best for HiED.

\item[RQ4] \textbf{Do the tested primary-selection strategies reduce the recorded selection disagreement?}

No tested strategy provides a clear and attributable improvement over Direct-Answer. Matched criterion-based re-selection with Nominate-then-Select reduces internal Top-1, and the other fixed-rule, pairwise, debate, and repeated-generation configurations do not consistently close the gap. This result is limited to the tested methods, prompts, and inference budgets.

\item[RQ5] \textbf{Does the stage-wise analysis remain useful under a second synthetic source?}

The same stage-wise output views remain applicable to MDD-5k and support the same form of disagreement localization. The largest external disagreement profile also contains a ranked and compatible benchmark-reference diagnosis while no benchmark-reference parent is committed as primary. However, the profile rates and compatibility inclusion differ from the internal trace and across archived MDD-5k lineages. The result supports portability of the analysis framework, not stable numerical behavior, superior generalization by HiED, or clinical validity.

\end{description}

\section{Future Work}

Within the current thesis project, the only retained follow-up study is the blinded LingxiDiag psychiatrist annotation described below. The other items are broader directions for independent future research and are not part of the completed experimental scope.

\paragraph{Complete and report the LingxiDiag psychiatrist annotation study.}

Psychiatrists will review selected synthetic disagreement cases, judge whether the transcript supports one primary diagnosis or remains insufficient, rank plausible diagnoses, and mark relevant criterion states. Their judgments can be compared with the dataset references and HiED records without treating any source as automatic clinical truth. Because the sample is purposively selected and synthetic, the completed study will characterize clinician interpretation of these cases rather than estimate clinical diagnostic accuracy.

\paragraph{Model direct comparisons among candidates.}

Future selectors may need to represent why one plausible diagnosis should be primary rather than only whether each diagnosis passes its own compatibility rule. Relevant relations may include symptom timing, illness course, episode structure, exclusionary causes, syndrome dominance, explanatory dependence, and comorbidity. These ideas require controlled studies that preserve the upstream candidate and criterion records.

\paragraph{Support missing-information and abstention decisions.}

A fixed transcript may not contain enough evidence to separate the leading diagnoses. Future systems could identify the unresolved distinction, propose a focused follow-up question, and allow an explicit insufficient-information, abstention, or referral result rather than forcing one primary diagnosis. These behaviors require separate evaluation and were not tested in this thesis.

\paragraph{Evaluate natural clinical data in independent future studies.}

Evaluation on natural psychiatric consultations, workflow impact, safety, fairness, privacy, and governance requires a separate clinical protocol and is outside the current thesis project. Such studies should use independent clinician adjudication, preserve uncertainty and disagreement, and should not assume that agreement with one benchmark diagnosis is equivalent to clinical correctness.

HiED's completed contribution is a stage-wise and inspectable output contract rather than a clinically validated diagnostic tool. The retained LingxiDiag annotation study will examine how clinicians interpret selected records; broader clinical validation and deployment remain independent future research.

'''


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_ch11_conclusions_revision.py <thesis.tex>")

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    start_marker = r"\chapter{Conclusions and Future Work}"
    end_marker = r"\appendix"

    if text.count(start_marker) != 1:
        raise RuntimeError(f"expected one Conclusions chapter marker, found {text.count(start_marker)}")
    if text.count(end_marker) != 1:
        raise RuntimeError(f"expected one appendix marker, found {text.count(end_marker)}")

    start = text.index(start_marker)
    end = text.index(end_marker, start)
    if start >= end:
        raise RuntimeError("invalid Conclusions/appendix ordering")

    revised = text[:start] + NEW_CHAPTER + text[end:]
    path.write_text(revised, encoding="utf-8")
    print(f"Applied Chapter 11 revision to {path}")


if __name__ == "__main__":
    main()
