#!/usr/bin/env python3
"""Apply the audited Chapter 4 metric-contract and split-provenance corrections."""

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
        "The 1,000-case internal held-out set was sampled from the 14,000-case training source using the first-listed projected parent label to approximately match the public-validation class distribution. A fixed random seed was used for reproducibility. The remaining 13,000 cases were used to train conventional baselines and build the retrieval index. The first-listed label served only as a stratification variable and was not treated as a clinically validated primary diagnosis. Case-ID checks confirmed that held-out cases were excluded from baseline training, the retrieval index, and all configuration-selection procedures. No additional semantic near-duplicate screening was performed.",
        "The 1,000-case internal held-out set was sampled from the 14,000-case training source using the first-listed projected parent label to approximately match the public-validation class distribution. A fixed random seed was used for reproducibility. The remaining 13,000 cases define the required training source for a leakage-controlled conventional baseline and were used to build the retained retrieval index. The first-listed label served only as a stratification variable and was not treated as a clinically validated primary diagnosis. Case-ID checks confirmed that held-out cases were excluded from the retained Route B system runs, the retrieval index, and all configuration-selection procedures. No additional semantic near-duplicate screening was performed. The preserved legacy S8 TF--IDF artifact predates this split convention: it was trained on the full 14,000-case source and evaluated on the disjoint public-validation split. It is therefore reported only as validation-split evidence and is not used as a Route B baseline.",
        "data-split provenance paragraph",
    )

    text = replace_once(
        text,
        "\\end{enumerate}\n\nSingle does not produce a standardized ranked differential diagnosis",
        "\\end{enumerate}\n\nWithin a method, Exact Match, Macro-F1, and Weighted-F1 are computed from the identical multilabel set $M(x)$. No metric-specific threshold or Top-1 substitution is used: a score threshold matters only insofar as it defines $M(x)$ before all three set-based measures are calculated.\n\nSingle does not produce a standardized ranked differential diagnosis",
        "shared emitted-set contract",
    )

    text = replace_once(
        text,
        "In the frozen repository snapshot used for this audit, no committed case-level prediction file matched the complete headline metric row for Majority, TF--IDF with logistic regression, or validation-selected Single Global Top-5 within the prespecified numerical tolerance. Their values are therefore retained as frozen aggregate results, and this thesis does not make new paired case-level, output-overlap, or output-cardinality claims from those rows.",
        "A subsequent repository-wide audit corrected an important filename and split-provenance gap. The preserved S8 file \\texttt{val\\_predictions.jsonl}, which the earlier exact-filename scan had skipped, contains 1,000 complete TF--IDF records with ranked class probabilities. Its stored emitted labels reproduce Top-1 0.610, ranked Top-3 0.919, Exact Match 0.553, Macro-F1 0.353572, and Weighted-F1 0.581003. Re-decoding the same probabilities with several explicit threshold rules changes Exact Match and F1 through output cardinality, but Top-1 remains 0.610. None of the audited decoders reproduces the legacy aggregate row 0.632/0.923/0.321/0.393/0.601.\n\nMore importantly, the S8 TF--IDF case IDs have zero overlap with the 1,000 case IDs in the canonical Route B HiED trace. The preserved S8 result is therefore a public-validation result, not a same-split Route B baseline. The legacy TF--IDF row is removed from the main Route B comparison below. No paired, same-split, or superiority claim is made from it. Complete headline-matching case-level files also remain unavailable for Majority and validation-selected Single Global Top-5, so contrasts involving those aggregate rows remain descriptive.",
        "case-level audit boundary",
    )

    old_design = """\\subsection{Same-Split Benchmark Positioning (RQ1)}

The validation-selected Single and HiED--DA configurations are evaluated together with the Majority baseline and TF--IDF with logistic regression on the same fixed 1,000-case internal held-out set. All rows use the parent-label projection and metric definitions in Chapter~\\ref{ch:data}.

Committed Top-1 Accuracy is the primary common measure because every configuration produces one committed primary diagnosis. Genuine ranked Top-3 is available for TF--IDF with logistic regression and HiED, whereas emitted-label hit@3 is reported separately for Single and Majority. Exact Match and F1 evaluate each method's complete emitted label set. The different three-label views and output cardinalities are therefore identified explicitly rather than treated as interchangeable.

The Majority baseline predicts the most frequent scoring parent in the training source. TF--IDF with logistic regression follows the character-level one-vs-rest configuration reported in Appendix~\\ref{app:supporting}. These comparisons are not component-controlled ablations: TF--IDF with logistic regression, Single, and HiED differ in training procedure, retrieval exposure, number of model calls, intermediate outputs, and output contract. Their performance differences describe complete configurations and cannot be attributed solely to multi-agent orchestration.

The current frozen snapshot contains a matching complete case-level output for the retained HiED--DA row but not for the complete headline rows of Majority, TF--IDF with logistic regression, or validation-selected Single Global Top-5. Accordingly, the RQ1 headline table is a same-split descriptive comparison. New paired confidence intervals, McNemar tests, prediction-overlap analyses, or output-cardinality claims are not inferred for contrasts involving those unmatched rows."""
    new_design = """\\subsection{Internal Benchmark Positioning and Split Boundary (RQ1)}

The validation-selected Single and HiED--DA aggregate results are reported on the fixed 1,000-case Route B internal held-out set together with the Majority aggregate baseline. All rows use the parent-label projection and metric definitions in Chapter~\\ref{ch:data}. A complete matching case-level file is retained for HiED--DA; the Majority and Single rows remain frozen aggregate results.

Committed Top-1 Accuracy is the primary common measure because every reported configuration produces one committed primary diagnosis. HiED provides a genuine ranked Top-3, whereas emitted-label hit@3 is reported separately for Single and Majority. Exact Match and F1 evaluate each method's complete emitted label set. The different three-label views and output cardinalities are therefore identified explicitly rather than treated as interchangeable.

No retained TF--IDF output covers the Route B case universe. The preserved lexical-classifier artifact instead covers the disjoint public-validation split and is reported separately as a metric-contract and same-source sensitivity analysis. It cannot be inserted into the Route B table or used to answer the conventional-classifier part of RQ1. A valid same-split comparison would require retraining after excluding every Route B case, freezing the emitted-set decoder without using Route B outcomes, and retaining the complete Route B case-level output.

The Route B rows are complete-system comparisons rather than component-controlled ablations. Single and HiED differ in retrieval exposure, number of model calls, intermediate outputs, and output contract. Their performance differences cannot be attributed solely to multi-agent orchestration. New paired confidence intervals, McNemar tests, prediction-overlap analyses, or output-cardinality claims are not inferred for contrasts whose matching case-level files were not retained."""
    text = replace_once(text, old_design, new_design, "RQ1 design subsection")

    text = replace_once(
        text,
        "This section addresses RQ1 on the fixed 1,000-case internal held-out set. Single uses the validation-selected global Top-5 configuration, and HiED--DA uses the validation-selected parent-balanced configuration. The comparison concerns complete systems under their stated output contracts; it is not a component-controlled test of multi-agent orchestration.",
        "This section addresses the Route B portion of RQ1 on the fixed 1,000-case internal held-out set. Single uses the validation-selected global Top-5 configuration, and HiED--DA uses the validation-selected parent-balanced configuration. The comparison concerns complete systems under their stated output contracts; it is not a component-controlled test of multi-agent orchestration. Because no retained TF--IDF output covers Route B, conventional-classifier evidence is presented separately and does not enter the same-split table.",
        "RQ1 results introduction",
    )

    text = replace_once(
        text,
        "\\caption{Main same-split comparison on the fixed 1,000-case internal held-out set using independently validation-selected configurations.}",
        "\\caption{Main Route B comparison on the fixed 1,000-case internal held-out set using independently validation-selected configurations. The TF--IDF baseline is excluded because no retained TF--IDF output covers this case universe.}",
        "Route B table caption",
    )

    text = replace_once(
        text,
        "TF--IDF + LR & None & Same-split lexical classifier & 0.632 & 0.923$^{\\mathrm{R}}$ & 0.321 & 0.393 & 0.601\\\\\n\\hline\n",
        "",
        "remove unsupported TF-IDF Route B row",
    )

    text = replace_once(
        text,
        "\\textit{Note.} $^{\\mathrm{R}}$ denotes genuine ranked Top-3 Accuracy: TF--IDF + LR uses its three highest-scoring classes, and HiED--DA uses the Diagnostician ranking. $^{\\mathrm{E}}$ denotes emitted-label hit@3: Majority emits one label, whereas Single uses its final emitted labels with the primary diagnosis first. The $\\mathrm{E}$ and $\\mathrm{R}$ values are different output views and are not interpreted as one common candidate-coverage measure.",
        "\\textit{Note.} $^{\\mathrm{R}}$ denotes HiED--DA's genuine ranked Top-3 Accuracy from the Diagnostician ranking. $^{\\mathrm{E}}$ denotes emitted-label hit@3: Majority emits one label, whereas Single uses its final emitted labels with the primary diagnosis first. The $\\mathrm{E}$ and $\\mathrm{R}$ values are different output views and are not interpreted as one common candidate-coverage measure. Only the HiED--DA row has a retained complete case-level file; the other Route B rows are frozen aggregates.",
        "Route B table note",
    )

    old_interpretation = """TF--IDF with logistic regression is the strongest same-corpus label predictor in Table~\\ref{tab:matched-baselines-retrieval}. It reaches 0.632 committed Top-1 Accuracy and 0.923 genuine ranked Top-3 Accuracy. Single and HiED--DA have nearly identical committed Top-1 values of 0.517 and 0.518. HiED--DA therefore does not establish an overall Top-1 advantage over either the lexical baseline or the validation-selected Single baseline.

The set-based measures describe a different part of the output contract. HiED--DA reaches 0.409 Exact Match, compared with 0.029 for Single, but this difference cannot be attributed only to the use of multiple agents because the systems construct and emit diagnostic sets differently. Macro-F1 and Weighted-F1 are likewise interpreted as complete-output measures rather than isolated tests of primary selection.

The aggregate Top-1 difference between HiED--DA and TF--IDF is $-0.114$. The frozen snapshot does not contain a TF--IDF case-level prediction file that matches the complete headline row, so no paired confidence interval, McNemar test, or case-overlap analysis is reported for this contrast. The case-level audit described in Section~\\ref{sec:metric-audit-boundary} does reproduce the HiED--DA values in Table~\\ref{tab:matched-baselines-retrieval} to the reported precision. Matching complete case-level files were not retained for the other three headline rows.

The strong same-corpus lexical result is consistent with substantial predictive information in transcript wording, label frequency, and other corpus-specific regularities. Chapter~\\ref{ch:external} separately tests whether lexical performance transfers across a second synthetic generation process. HiED's distinct empirical contribution in the internal analysis is not higher final-label accuracy, but the additional recorded artifacts: a genuine ranked differential, criterion states, a criterion-compatible set, and a committed-primary record."""
    new_interpretation = """Single and HiED--DA have nearly identical committed Top-1 values of 0.517 and 0.518 on Route B. HiED--DA therefore does not establish an overall Top-1 advantage over the validation-selected Single baseline. The set-based measures describe another part of the output contract: HiED--DA reaches 0.409 Exact Match, compared with 0.029 for Single, but this difference cannot be attributed only to the use of multiple agents because the systems construct and emit diagnostic sets differently. Macro-F1 and Weighted-F1 are likewise complete-output measures rather than isolated tests of primary selection.

\\begin{table}[H]
\\centering
\\caption{Preserved TF--IDF metric-contract audit on the public-validation split ($N=1000$). These are not Route B headline results.}
\\label{tab:tfidf-validation-contract-audit}
\\small
\\begin{adjustbox}{max width=\\textwidth}
\\begin{tabular}{|l|c|c|c|c|c|c|}
\\hline
Emitted-set decoder & Top-1 & Ranked Top-3 & Exact Match & Macro-F1 & Weighted-F1 & Mean set size\\\\
\\hline
Stored emitted set (singleton) & 0.610 & 0.919 & 0.553 & 0.354 & 0.581 & 1.000\\\\
\\hline
All labels with $p\\geq0.50$ (post-hoc sensitivity) & 0.610 & 0.919 & 0.327 & 0.404 & 0.603 & 1.614\\\\
\\hline
\\end{tabular}
\\end{adjustbox}
\\parbox{0.96\\textwidth}{\\footnotesize
\\textit{Note.} Both rows use the same preserved 1,000 public-validation cases and the same primary and ranked predictions. Exact Match, Macro-F1, and Weighted-F1 use one identical emitted set within each row. The thresholded row is a diagnostic sensitivity, not a validation-selected replacement result. The previously printed aggregate row 0.632/0.923/0.321/0.393/0.601 is not reproduced by the retained case-level output or any audited decoder and is therefore removed from the Route B comparison.}
\\end{table}

The audit shows why Exact Match and F1 need not have parallel trends: changing the emitted-set decoder changes output cardinality, while all three set measures still consume the same set. It also shows that decoder choice cannot explain the legacy Top-1 difference, because Top-1 remains 0.610 under every audited set decoder. The decisive limitation is population provenance: the preserved TF--IDF cases have zero case-ID overlap with Route B.

Accordingly, no numerical Route B contrast between HiED--DA and TF--IDF is reported. The preserved validation result supports only the narrower observation that lexical features can be predictive within the LingxiDiag generation source. Chapter~\\ref{ch:external} tests whether such lexical performance transfers across a second synthetic generation process. HiED's distinct empirical contribution in the Route B analysis is the additional recorded artifacts: a genuine ranked differential, criterion states, a criterion-compatible set, and a committed-primary record."""
    text = replace_once(text, old_interpretation, new_interpretation, "RQ1 interpretation and TF-IDF audit table")

    text = replace_once(
        text,
        "Under the common internal split and parent-label mapping, TF--IDF with logistic regression provides the strongest final label prediction. Single and HiED--DA have almost identical committed Top-1 performance. HiED does not establish an accuracy advantage, but it provides the diagnostic records needed for the stage-wise analyses below.",
        "On the common Route B internal split, Single and HiED--DA have almost identical committed Top-1 performance, and HiED does not establish an accuracy advantage over Single. The conventional-classifier part of RQ1 remains unresolved because no retained TF--IDF output covers Route B. The separate public-validation TF--IDF audit shows strong same-source lexical prediction but cannot be interpreted as a same-split comparison. HiED provides the diagnostic records needed for the stage-wise analyses below.",
        "RQ1 answer",
    )

    text = replace_once(
        text,
        "The internal results give five main answers. Retrieval improves the Single baseline more clearly than HiED, and parent-balanced retrieval remains the primary HiED configuration because of the validation contract rather than the held-out ranking. TF--IDF with logistic regression is the strongest same-corpus label predictor, while Single and HiED have almost identical committed Top-1 performance. HiED nevertheless exposes a large difference between candidate availability, criterion compatibility, and committed-primary agreement: 272 of 915 checker-eligible cases contain a benchmark gold parent in both the Top-3 and compatible set but commit another diagnosis. The tested primary-selection interventions do not provide a clear attributable improvement over DA. Finally, HiED's Top-3 coverage is comparatively stable across the evaluated Qwen3 sizes, while the remaining disagreements are concentrated toward a small number of diagnostic directions. Chapter~\\ref{ch:external} examines whether these patterns persist under external synthetic distribution shift.",
        "The internal results give five main answers. Retrieval improves the Single baseline more clearly than HiED, and parent-balanced retrieval remains the primary HiED configuration because of the validation contract rather than the held-out ranking. Single and HiED have almost identical committed Top-1 performance on Route B; no retained TF--IDF output covers that split, so no same-split lexical-superiority claim is made. The separate public-validation TF--IDF audit shows substantial same-source lexical predictability but is kept outside the Route B table. HiED nevertheless exposes a large difference between candidate availability, criterion compatibility, and committed-primary agreement: 272 of 915 checker-eligible cases contain a benchmark gold parent in both the Top-3 and compatible set but commit another diagnosis. The tested primary-selection interventions do not provide a clear attributable improvement over DA. Finally, HiED's Top-3 coverage is comparatively stable across the evaluated Qwen3 sizes, while the remaining disagreements are concentrated toward a small number of diagnostic directions. Chapter~\\ref{ch:external} examines whether these patterns persist under external synthetic distribution shift.",
        "Chapter 5 summary",
    )

    text = replace_once(
        text,
        "The lexical transfer analysis uses a separately preserved full-corpus TF--IDF with logistic-regression matrix. Table~\\ref{tab:lexical-transfer-rewrite} reports Top-1 and genuine Top-3 values under that artifact's twelve-class parent-label contract.",
        "The lexical transfer analysis uses a separately preserved full-corpus TF--IDF with logistic-regression matrix. Its LingxiDiag evaluation population is the public-validation split rather than Route B. Table~\\ref{tab:lexical-transfer-rewrite} reports Top-1 and genuine Top-3 values under that artifact's twelve-class parent-label contract.",
        "external lexical population",
    )
    text = text.replace("LingxiDiag held-out & 1,000", "LingxiDiag public validation & 1,000")
    text = replace_once(
        text,
        "\\textit{Note.} These are full-corpus transfer runs. They are not the previously reported F32--F41 subset values and should not be interpreted as that binary experiment.}",
        "\\textit{Note.} These are full-corpus transfer runs. The LingxiDiag evaluation rows use the public-validation split, not the Route B internal held-out set. They are not the previously reported F32--F41 subset values and should not be interpreted as that binary experiment.}",
        "external lexical note",
    )

    text = replace_once(
        text,
        "The results support a stage-wise interpretation of HiED rather than an accuracy-leading claim. TF--IDF with logistic regression is the strongest same-source label predictor in the main internal comparison, and Single and HiED have almost the same committed Top-1 result. HiED's distinct contribution is the set of recorded outputs that makes candidate generation, criterion checking, compatibility analysis, and primary commitment separately visible.",
        "The results support a stage-wise interpretation of HiED rather than an accuracy-leading claim. Single and HiED have almost the same committed Top-1 result on Route B. A separate public-validation TF--IDF audit shows strong same-source lexical prediction, but no retained TF--IDF output covers Route B, so it is not treated as a same-split superiority result. HiED's distinct contribution is the set of recorded outputs that makes candidate generation, criterion checking, compatibility analysis, and primary commitment separately visible.",
        "discussion opening",
    )

    text = replace_once(
        text,
        "HiED does not establish the best final-label accuracy. On the internal held-out set, TF--IDF with logistic regression is the strongest same-source label predictor, while Single and HiED have almost identical committed Top-1 results. HiED's main technical value is that its recorded outputs allow benchmark disagreement to be divided into different profiles.",
        "HiED does not establish the best final-label accuracy. On the Route B internal held-out set, Single and HiED have almost identical committed Top-1 results. The retained TF--IDF evidence comes from the disjoint public-validation split, so the thesis does not claim a same-split conventional-classifier ranking. HiED's main technical value is that its recorded outputs allow benchmark disagreement to be divided into different profiles.",
        "conclusion findings",
    )

    text = replace_once(
        text,
        "\\item[RQ1] \\textbf{How does HiED perform relative to conventional classification and a Single LLM on the same internal split and parent-label evaluation?}\n\nTF--IDF with logistic regression provides the strongest same-source final-label prediction. Single and HiED have almost identical committed Top-1 values. HiED does not establish an overall accuracy advantage, but it provides a genuine ranked differential, criterion states, a criterion-compatible set, and a final selection record for stage-wise analysis.",
        "\\item[RQ1] \\textbf{How does HiED compare with a Single LLM on the same internal split, and what conventional-classifier evidence is available?}\n\nOn Route B, Single and HiED have almost identical committed Top-1 values, so HiED does not establish an overall accuracy advantage over Single. No retained TF--IDF output covers Route B; the preserved TF--IDF result is a public-validation analysis and cannot complete the same-split conventional-classifier comparison. HiED provides a genuine ranked differential, criterion states, a criterion-compatible set, and a final selection record for stage-wise analysis.",
        "final RQ1 question and answer",
    )

    text = replace_once(
        text,
        "{\\footnotesize\n\\noindent\\textit{TF--IDF baseline configuration:} The model is trained on 13,000 source cases. It uses character-boundary 1--2-grams, at most 10,000 features, \\texttt{min\\_df=2}, \\texttt{max\\_df=0.95}, and sublinear term frequency. Twelve class-balanced one-vs-rest L-BFGS logistic-regression classifiers use $C=1.0$ and a 2,000-iteration limit. Their probabilities define the ranked labels and thresholded multilabel output.\n\\par}",
        "{\\footnotesize\n\\noindent\\textit{Required Route B TF--IDF protocol:} A valid same-split baseline must train on the 13,000 source cases remaining after all Route B IDs are excluded. It uses character-boundary 1--2-grams, at most 10,000 features, \\texttt{min\\_df=2}, \\texttt{max\\_df=0.95}, and sublinear term frequency. Twelve class-balanced one-vs-rest L-BFGS logistic-regression classifiers use $C=1.0$ and a 2,000-iteration limit. The emitted-set decoder must be frozen without Route B outcomes; argmax defines the primary, class scores define the genuine ranking, and one identical decoded set is used for Exact Match, Macro-F1, and Weighted-F1.\n\n\\noindent\\textit{Preserved legacy S8 artifact:} The historical script trained on all 14,000 training-source cases and evaluated the 1,000 public-validation cases. It defined the primary by argmax and optionally added only the second-ranked class when its rounded probability was at least 0.30. The retained S8 prediction file contains singleton emitted sets and has zero case-ID overlap with Route B. It is therefore used only for the validation-split audit in Table~\\ref{tab:tfidf-validation-contract-audit}; no Route B TF--IDF metric is reported.\n\\par}",
        "appendix TF-IDF provenance",
    )

    forbidden = [
        "TF--IDF + LR & None & Same-split lexical classifier",
        "TF--IDF with logistic regression is the strongest same-corpus label predictor",
        "TF--IDF with logistic regression is the strongest same-source label predictor in the main internal comparison",
        "Under the common internal split and parent-label mapping, TF--IDF",
        "The aggregate Top-1 difference between HiED--DA and TF--IDF",
    ]
    remaining = [phrase for phrase in forbidden if phrase in text]
    if remaining:
        raise RuntimeError(f"unsupported same-split claims remain: {remaining}")

    if text.count("LingxiDiag public validation & 1,000") != 2:
        raise RuntimeError("expected two corrected LingxiDiag public-validation transfer rows")

    PATH.write_text(text, encoding="utf-8")
    print("Applied Chapter 4 metric-contract and split-provenance corrections.")


if __name__ == "__main__":
    main()
