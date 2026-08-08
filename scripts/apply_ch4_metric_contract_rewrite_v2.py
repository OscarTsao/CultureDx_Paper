from __future__ import annotations

from pathlib import Path


PREDICTION_METRICS_SECTION = r"""\section{Prediction Views and Metrics}
\label{sec:prediction-metrics}

The evaluator keeps five recorded output views separate:

\begin{enumerate}[label=(\arabic*)]
\item The \emph{primary view}, $p_1(x)$, is the committed primary diagnosis.
\item The \emph{ranked view}, $R_3(x)$, contains the first three distinct parent labels in a method's genuine ranked output. TF--IDF with logistic regression obtains this view from ranked class scores. HiED obtains it from the recorded Diagnostician ranking, before DA or NtS finalization.
\item The \emph{emitted-label sequence}, $E_3(x)$, contains the first three distinct parent labels available in the final emitted output, with the committed primary diagnosis placed first. This view is used only when aggregate benchmark reporting requires a three-label hit rate but the method does not produce a genuine ranking.
\item The \emph{compatibility view}, $L(x)$, is the set of scoring parent labels classified as criterion-compatible by the Compatibility Auditor under the configured operational rules.
\item The \emph{multilabel view}, $M(x)$, is the complete set of emitted parent labels used for Exact Match and F1. For DA, it contains the committed primary diagnosis and any emitted comorbid parent label. For a single-label method, it contains one label.
\end{enumerate}

Single does not produce a standardized ranked differential diagnosis, so it has no genuine $R_3(x)$ view. For continuity with the aggregate LingxiDiagBench reporting convention, this thesis separately reports an \emph{emitted-label hit@3} from $E_3(x)$ for Single. The sequence may contain an optional additional diagnosis that was emitted as a comorbidity rather than ranked as a differential alternative. It is therefore not interpreted as candidate coverage and is not used to define $D_3$. The Majority baseline emits one label, so its emitted-label hit@3 is numerically identical to its Top-1 Accuracy.

Because a case may contain more than one gold label, each hit measure counts a case as correct when at least one projected benchmark gold label appears in the evaluated view. Exact Match, also called subset accuracy, instead requires the complete predicted label set to equal the complete gold-label set. These are benchmark-agreement measures, not independent measures of the patient's true clinical diagnosis.

For example, suppose that the projected gold-label set contains F41, while a genuine ranking places F32 first and F41.1 second. Because F41.1 is projected to its scoring parent F41, the case is incorrect under committed Top-1 evaluation but correct under ranked Top-3 evaluation.

DA may emit a committed primary diagnosis and one optional comorbid diagnosis, whereas NtS emits one committed primary diagnosis. Their Top-1 comparison therefore evaluates the committed primary directly, but differences in Exact Match, Macro-F1, or Weighted-F1 also reflect output cardinality and cannot be interpreted as isolated effects of primary re-selection.

Table~\ref{tab:metric-contract} summarizes which recorded output view is evaluated by each measure. The subsequent equations give the case-level definitions used by the scoring implementation.

\begin{table}[H]
\centering
\caption{Definitions of the main evaluation measures by output view.}
\label{tab:metric-contract}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.2cm}|>{\raggedright\arraybackslash}p{3.8cm}|>{\raggedright\arraybackslash}X|}
\hline
Measure & Evaluated output & Definition\\
\hline
Top-1 Accuracy & Committed primary, $p_1(x)$ & $p_1(x)\in G(x)$\\
\hline
Ranked Top-3 Accuracy & Genuine ranked candidates, $R_3(x)$ & $R_3(x)\cap G(x)\neq\varnothing$\\
\hline
Emitted-label hit@3 & Emitted-label sequence, $E_3(x)$ & $E_3(x)\cap G(x)\neq\varnothing$\\
\hline
Gold-label inclusion & Criterion-compatible set, $L(x)$ & $L(x)\cap G(x)\neq\varnothing$\\
\hline
Exact Match & Complete emitted set, $M(x)$ & $M(x)=G(x)$\\
\hline
Macro-F1 & Complete emitted set, $M(x)$ & Unweighted mean of the fixed-class one-vs-rest F1 scores\\
\hline
Weighted-F1 & Complete emitted set, $M(x)$ & The same label-level F1 scores weighted by gold-label support\\
\hline
\end{tabularx}
\end{table}

Top-1 and any reported three-label hit measure are computed over all 1,000 internal test cases. Ranked Top-3 is reported only for a method with a genuine ranked view. Gold-label inclusion in the criterion-compatible set is computed over the 915 cases with at least one non-\emph{Others} gold parent covered by a corresponding Criterion Checker.

\[
\mathrm{Top\text{-}1\ Accuracy}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[p_1(x)\in G(x)],
\]
\[
\mathrm{Ranked\ Top\text{-}3\ Accuracy}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[R_3(x)\cap G(x)\neq\varnothing],
\]
\[
\mathrm{Emitted\text{-}label\ hit@3}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[E_3(x)\cap G(x)\neq\varnothing],
\]
\[
\mathrm{Exact\ Match}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[M(x)=G(x)].
\]

Let the fixed scoring universe be
\[
\mathcal{Y}=\{\mathrm{F20},\mathrm{F31},\mathrm{F32},\mathrm{F39},\mathrm{F41},\mathrm{F42},\mathrm{F43},\mathrm{F45},\mathrm{F51},\mathrm{F98},\mathrm{Z71},\mathrm{Others}\}.
\]
For class $c\in\mathcal{Y}$, define $y_{x,c}=\mathbb{1}[c\in G(x)]$ and $\hat{y}_{x,c}=\mathbb{1}[c\in M(x)]$. The one-vs-rest counts are
\[
\mathrm{TP}_c=\sum_x y_{x,c}\hat{y}_{x,c},\qquad
\mathrm{FP}_c=\sum_x (1-y_{x,c})\hat{y}_{x,c},\qquad
\mathrm{FN}_c=\sum_x y_{x,c}(1-\hat{y}_{x,c}).
\]
The class-level F1 score is
\[
\mathrm{F1}_c=
\begin{cases}
\dfrac{2\mathrm{TP}_c}{2\mathrm{TP}_c+\mathrm{FP}_c+\mathrm{FN}_c}, & 2\mathrm{TP}_c+\mathrm{FP}_c+\mathrm{FN}_c>0,\\[6pt]
0, & \text{otherwise}.
\end{cases}
\]
This zero case matches the scoring implementation's \texttt{zero\_division=0} contract: a class with no positive support and no positive prediction contributes zero rather than being removed from the fixed class universe. Macro-F1 and Weighted-F1 are then
\[
\mathrm{Macro\text{-}F1}=\frac{1}{|\mathcal{Y}|}\sum_{c\in\mathcal{Y}}\mathrm{F1}_c,
\]
\[
\mathrm{Weighted\text{-}F1}=\frac{\sum_{c\in\mathcal{Y}} n_c\,\mathrm{F1}_c}{\sum_{c\in\mathcal{Y}} n_c},
\qquad n_c=\sum_x y_{x,c}.
\]
Macro-F1 gives equal weight to all twelve scoring classes, including rare classes and \emph{Others}. Weighted-F1 gives more influence to classes with greater gold support and is therefore driven mainly by the frequent F32 and F41 labels in this study. Both measures evaluate the complete emitted set $M(x)$ and are sensitive to how many diagnoses a method emits.

\subsection{Case-Level Metric Audit and Recalculation Boundary}
\label{sec:metric-audit-boundary}

The frozen 1,000-case output of the validation-selected HiED--DA parent-balanced configuration was independently rescored using the definitions above. The recalculation produced Top-1 Accuracy 0.518000, ranked Top-3 Accuracy 0.802000, Exact Match 0.409000, Macro-F1 0.177577, and Weighted-F1 0.433738. These values reproduce the reported three-decimal results of 0.518, 0.802, 0.409, 0.178, and 0.434.

The same audit found a mean gold-set size of 1.093 and a mean predicted-set size of 1.136. HiED--DA emitted one diagnosis for 864 cases and two diagnoses for 136 cases. These counts confirm that Exact Match, Macro-F1, and Weighted-F1 in the main table are complete-set measures rather than primary-only measures. Primary-only F1 was also calculated as an exploratory diagnostic check, but it is not substituted for the prespecified set-based F1 values.

In the frozen repository snapshot used for this audit, no committed case-level prediction file matched the complete headline metric row for Majority, TF--IDF with logistic regression, or validation-selected Single Global Top-5 within the prespecified numerical tolerance. Their values are therefore retained as frozen aggregate results, and this thesis does not make new paired case-level, output-overlap, or output-cardinality claims from those rows.

First-listed-label agreement compares the committed diagnosis only with the first-listed projected gold parent. It is used for the confusion matrix but not for the main result. It may differ from any-gold Top-1 Accuracy when a case contains more than one gold parent label.

"""


VALIDATION_CONFIGURATION_TABLE = r"""\begin{table}[H]
\centering
\caption{Validation-selected thesis configurations and published LingxiDiagBench context for the twelve-category diagnostic task~\citep{xu2026lingxidiagbench}.}
\label{tab:validation-configuration-matrix}
\small
\begin{adjustbox}{max width=\textwidth}
\begin{tabular}{|l|l|c|c|c|c|c|}
\hline
Method & Retrieval or source & Top-1 & \shortstack{Reported three-label\\coverage} & Exact Match & Macro-F1 & Weighted-F1\\
\hline
\multicolumn{7}{|c|}{\textbf{Validation-selected thesis configurations}}\\
\hline
Single & Global Top-5 & 0.519 & 0.725$^{\mathrm{E}}$ & 0.030 & 0.209 & 0.456\\
HiED--DA & Parent-balanced & 0.523 & 0.800$^{\mathrm{R}}$ & 0.428 & 0.181 & 0.440\\
\hline
\multicolumn{7}{|c|}{\textbf{Published LingxiDiagBench static results}}\\
\hline
TF--IDF + LR & Published benchmark & 0.496 & 0.645 & 0.268 & 0.295 & 0.520\\
GPT-5-Mini & Published benchmark & 0.487 & 0.505 & 0.409 & 0.188 & 0.418\\
Qwen3-32B & Published benchmark & 0.470 & 0.566 & 0.241 & 0.188 & 0.431\\
\hline
\end{tabular}
\end{adjustbox}
\parbox{0.96\textwidth}{\footnotesize
\textit{Note.} $^{\mathrm{E}}$ denotes emitted-label hit@3 and $^{\mathrm{R}}$ denotes genuine ranked Top-3 Accuracy. The published rows reproduce the source paper's reported Top-3 values under its original metric contract and are not reclassified as either thesis output view.
}
\end{table}
"""


MAIN_COMPARISON_TABLE = r"""\begin{table}[H]
\centering
\caption{Main same-split comparison on the fixed 1,000-case internal held-out set using independently validation-selected configurations.}
\label{tab:matched-baselines-retrieval}
\small
\begin{adjustbox}{max width=\textwidth}
\begin{tabular}{|l|l|>{\raggedright\arraybackslash}p{3.5cm}|c|c|c|c|c|}
\hline
System & Retrieval & Output role & Top-1 & \shortstack{Three-label\\coverage} & Exact Match & Macro-F1 & Weighted-F1\\
\hline
Majority & None & Frequency baseline with one emitted label & 0.398 & 0.398$^{\mathrm{E}}$ & 0.327 & 0.047 & 0.207\\
\hline
TF--IDF + LR & None & Same-split lexical classifier & 0.632 & 0.923$^{\mathrm{R}}$ & 0.321 & 0.393 & 0.601\\
\hline
Single & Global Top-5 & Validation-selected single-call LLM baseline & 0.517 & 0.748$^{\mathrm{E}}$ & 0.029 & 0.224 & 0.447\\
\hline
HiED--DA & Parent-balanced & Validation-selected proposed system & 0.518 & 0.802$^{\mathrm{R}}$ & 0.409 & 0.178 & 0.434\\
\hline
\end{tabular}
\end{adjustbox}
\parbox{0.96\textwidth}{\footnotesize
\textit{Note.} $^{\mathrm{R}}$ denotes genuine ranked Top-3 Accuracy: TF--IDF + LR uses its three highest-scoring classes, and HiED--DA uses the Diagnostician ranking. $^{\mathrm{E}}$ denotes emitted-label hit@3: Majority emits only one label, whereas Single uses its final emitted labels with the primary diagnosis first. The $\mathrm{E}$ and $\mathrm{R}$ values are different output views and are not interpreted as one common candidate-coverage measure.
}
\end{table}
"""


RETRIEVAL_RESULTS_TABLE = r"""\begin{table}[H]
\centering
\caption{Retrieval-strategy results on the public-validation and fixed internal test splits. Configurations marked with $\dagger$ were selected using validation results. Test-set results are post-selection evaluations and do not revise the selected configurations.}
\label{tab:retrieval-results}
\small

\textbf{Panel A. Single}

\vspace{0.3em}

\begin{adjustbox}{max width=\textwidth}
\begin{tabular}{|l|l|c|c|c|c|c|}
\hline
Split & Retrieval & Top-1 & Emitted hit@3 & Exact Match & Macro-F1 & Weighted-F1\\
\hline
Validation & None & 0.466 & 0.580 & 0.016 & 0.174 & 0.429\\
Validation & Global Top-5$^{\dagger}$ & 0.519 & 0.725 & 0.030 & 0.209 & 0.456\\
Validation & Parent-balanced & 0.507 & 0.741 & 0.016 & 0.195 & 0.437\\
\hline
Test & None & 0.466 & 0.648 & 0.017 & 0.183 & 0.426\\
Test & Global Top-5$^{\dagger}$ & 0.517 & 0.748 & 0.029 & 0.224 & 0.447\\
Test & Parent-balanced & 0.508 & 0.757 & 0.011 & 0.192 & 0.433\\
\hline
\end{tabular}
\end{adjustbox}

\vspace{0.8em}

\textbf{Panel B. HiED--DA}

\vspace{0.3em}

\begin{adjustbox}{max width=\textwidth}
\begin{tabular}{|l|l|c|c|c|c|c|}
\hline
Split & Retrieval & Top-1 & Ranked Top-3 & Exact Match & Macro-F1 & Weighted-F1\\
\hline
Validation & None & 0.509 & 0.792 & 0.456 & 0.173 & 0.428\\
Validation & Global Top-5 & 0.525 & 0.797 & 0.432 & 0.178 & 0.435\\
Validation & Parent-balanced$^{\dagger}$ & 0.523 & 0.800 & 0.428 & 0.181 & 0.440\\
\hline
Test & None & 0.510 & 0.786 & 0.404 & 0.174 & 0.437\\
Test & Global Top-5 & 0.524 & 0.815 & 0.435 & 0.196 & 0.437\\
Test & Parent-balanced$^{\dagger}$ & 0.518 & 0.802 & 0.409 & 0.178 & 0.434\\
\hline
\end{tabular}
\end{adjustbox}

\parbox{0.96\textwidth}{\footnotesize
\textit{Note.} Panel A reports Single's emitted-label hit@3 from the available final labels, with the primary diagnosis first. It is not a genuine ranked differential and is not used for $D_3$. Panel B reports HiED--DA's genuine ranked Top-3 Accuracy from the Diagnostician ranking. Selection used only the public-validation split and compared each architecture with itself.
}
\end{table}
"""


def replace_once(text: str, old: str, new: str, description: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one {description}; found {count}")
    return text.replace(old, new, 1)


def replace_between(
    text: str,
    start_marker: str,
    end_marker: str,
    replacement: str,
    description: str,
    *,
    include_end: bool = False,
) -> str:
    if text.count(start_marker) != 1:
        raise RuntimeError(f"Expected exactly one start marker for {description}")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    if include_end:
        end += len(end_marker)
    return text[:start] + replacement + text[end:]


def main() -> None:
    candidates = [Path("school/main.tex"), Path("paper/school/HiED_school_version.tex")]
    target = next((path for path in candidates if path.exists()), None)
    if target is None:
        raise FileNotFoundError("Could not locate the School thesis source")

    text = target.read_text(encoding="utf-8")
    if "Case-Level Metric Audit and Recalculation Boundary" in text:
        print(f"{target} already contains the Chapter 4 metric-contract rewrite")
        return

    before_guard = text.count(r"\newif\ifshowcomments")
    before_showcomments = text.count(r"\showcommentstrue") + text.count(r"\showcommentsfalse")
    before_ct = text.count(r"\ct{")
    before_wl = text.count(r"\wl{")

    old_mdd = (
        "The evaluated release contains 925 patient-level cases. Under HiED's main configured output space defined in Section~\\ref{sec:gold-label-conventions}, a case is defined as \\emph{in scope} when at least one projected benchmark gold diagnosis can be emitted by the system and as \\emph{out of scope} when none of its projected gold diagnoses is represented in that output space. Among the 925 external cases, 878 are in scope and the remaining 47 are out of scope. Because MDD-5k transcripts are generally longer than those in LingxiDiag-16K, the same prompt-budget rule defined in Chapter~\\ref{ch:architecture} is applied to the external evaluation. MDD-5k is used as an external synthetic benchmark and does not constitute validation on real patient transcripts."
    )
    new_mdd = (
        "The evaluated release contains 925 patient-level cases. Under HiED's main configured output space defined in Section~\\ref{sec:gold-label-conventions}, a case is defined as \\emph{in scope} when at least one projected benchmark gold diagnosis can be emitted by the system and as \\emph{out of scope} when none of its projected gold diagnoses is represented in that output space. Among the 925 external cases, 878 are in scope and the remaining 47 are out of scope. Because MDD-5k transcripts are generally longer than those in LingxiDiag-16K, the external runs use the same deterministic, turn-preserving prompt-budget procedure as the internal runs; the implementation rule is reported in Appendix~\\ref{app:supporting}. MDD-5k is used as an external synthetic benchmark and does not constitute validation on real patient transcripts."
    )
    text = replace_once(text, old_mdd, new_mdd, "MDD-5k prompt-budget paragraph")

    section_start = r"\section{Prediction Views and Metrics}"
    next_section = r"\section{Case-Level Indicators for Disagreement Localization}"
    prediction_start = text.index(section_start)
    prediction_end = text.index(next_section, prediction_start)
    old_prediction_section = text[prediction_start:prediction_end]
    if r"\ct{" in old_prediction_section or r"\wl{" in old_prediction_section:
        raise RuntimeError("Advisor comments were found inside the replaced metric section")
    text = text[:prediction_start] + PREDICTION_METRICS_SECTION + text[prediction_end:]

    old_rq3 = (
        "For each architecture, retrieval selection followed a prespecified majority-based promotion rule over five validation metrics: Top-1 Accuracy, Top-3 Accuracy (genuine ranked Top-3 for HiED--DA and benchmark-defined emitted-label Top-3 for Single), Exact Match, Macro-F1, and Weighted-F1. A candidate configuration replaced the currently retained configuration only when it achieved higher values on more than half of these five metrics; otherwise, the currently retained configuration was kept. Once selected, each configuration was frozen before evaluation on the internal held-out set. Validation results were used only for configuration selection and were not treated as independent test estimates. Held-out results were not used to revise the selected configurations."
    )
    new_rq3 = (
        "For each architecture, retrieval selection followed a prespecified majority-based promotion rule over five validation metrics: Top-1 Accuracy, one architecture-specific three-label coverage measure, Exact Match, Macro-F1, and Weighted-F1. The three-label measure was emitted-label hit@3 for Single and genuine ranked Top-3 Accuracy for HiED--DA. A candidate configuration replaced the currently retained configuration only when it achieved higher values on more than half of these five metrics; otherwise, the currently retained configuration was kept. This coverage measure was used only for within-architecture selection: emitted-label hit@3 and ranked Top-3 are not treated as the same quantity across architectures. Once selected, each configuration was frozen before evaluation on the internal held-out set. Validation results were used only for configuration selection and were not treated as independent test estimates. Held-out results were not used to revise the selected configurations."
    )
    text = replace_once(text, old_rq3, new_rq3, "RQ3 selection-contract paragraph")

    old_same_split = (
        "Committed Top-1 Accuracy is the primary comparison metric because every evaluated configuration produces one committed primary diagnosis. Genuine Top-3 and multilabel measures are reported only when the corresponding output view is available. Single does not produce a genuine ranked differential diagnosis; its benchmark-defined Top-3, when reported for compatibility with LingxiDiagBench, is computed from the available emitted-label list and is not interpreted as ranked candidate coverage."
    )
    new_same_split = (
        "Committed Top-1 Accuracy is the primary comparison metric because every evaluated configuration produces one committed primary diagnosis. Genuine ranked Top-3 is available for TF--IDF with logistic regression and HiED, whereas emitted-label hit@3 is reported separately for Single and Majority. The emitted-label and ranked measures are displayed for completeness but are not interpreted as one common cross-architecture candidate-coverage measure. Exact Match and F1 are reported from each method's complete emitted label set under the contract defined in Section~\\ref{sec:prediction-metrics}."
    )
    text = replace_once(text, old_same_split, new_same_split, "RQ1 common-metric paragraph")

    validation_start = r"\begin{table}[H]
\centering
\caption{Validation-selected thesis configurations"
    validation_end = r"\end{table}"
    text = replace_between(
        text,
        validation_start,
        validation_end,
        VALIDATION_CONFIGURATION_TABLE,
        "validation configuration table",
        include_end=True,
    )

    text = replace_once(
        text,
        "The table reports committed Top-1 and identifies the source of each Top-3 value.",
        "The table reports committed Top-1 and identifies the output view used for each three-label coverage value.",
        "main-table introduction sentence",
    )

    main_start = r"\begin{table}[H]
\centering
\caption{Main same-split comparison"
    text = replace_between(
        text,
        main_start,
        r"\end{table}",
        MAIN_COMPARISON_TABLE,
        "main same-split comparison table",
        include_end=True,
    )

    old_main_narrative = (
        "As shown in Table~\\ref{tab:matched-baselines-retrieval}, TF--IDF + logistic regression has the highest Top-1 and Top-3 values, at 0.632 and 0.923. Single and HiED--DA achieve nearly identical committed Top-1 point estimates of 0.517 and 0.518, while their non-equivalent Top-3 measures are 0.748 and 0.802. The Top-1 difference between HiED--DA and TF--IDF is $-0.114$ (95\\% CI [$-0.150$, $-0.079$]); the evaluated HiED configuration therefore does not provide an overall accuracy advantage on this benchmark."
    )
    new_main_narrative = (
        "As shown in Table~\\ref{tab:matched-baselines-retrieval}, TF--IDF + logistic regression has the highest committed Top-1 Accuracy at 0.632 and the highest genuine ranked three-label coverage at 0.923. Single and HiED--DA achieve nearly identical committed Top-1 point estimates of 0.517 and 0.518. Single's 0.748 value is emitted-label hit@3, whereas HiED--DA's 0.802 value is genuine ranked Top-3 Accuracy; these values are not compared as one common candidate-coverage measure. The Top-1 difference between HiED--DA and TF--IDF is $-0.114$ (95\\% CI [$-0.150$, $-0.079$]); the evaluated HiED configuration therefore does not provide an overall accuracy advantage on this benchmark."
    )
    text = replace_once(text, old_main_narrative, new_main_narrative, "main comparison narrative")

    old_value_paragraph = (
        "HiED's additional empirical value lies instead in the diagnostic artifacts unavailable from the direct baselines: an explicit ranked differential, criterion-level outputs, compatibility decisions, and a traceable committed diagnosis. The following sections compare candidate detection, gold-label inclusion, and committed-primary agreement."
    )
    new_value_paragraph = (
        "The case-level recalculation described in Section~\\ref{sec:metric-audit-boundary} exactly reproduced the reported HiED--DA values to three decimal places. The current frozen snapshot did not provide matching committed case-level files for the other three headline rows, so no new paired case-level comparison is inferred from their aggregate values. HiED's additional empirical value lies instead in the diagnostic artifacts unavailable from the direct baselines: an explicit ranked differential, criterion-level outputs, compatibility decisions, and a traceable committed diagnosis. The following sections compare candidate detection, gold-label inclusion, and committed-primary agreement."
    )
    text = replace_once(text, old_value_paragraph, new_value_paragraph, "metric-audit result paragraph")

    old_panels = (
        "The panels remain separate because their Top-3 measures represent different output views. Panel A reports Single's benchmark-defined hit rate over the available emitted labels, whereas Panel B reports HiED--DA's genuine ranked Top-3 differential."
    )
    new_panels = (
        "The panels remain separate because their three-label measures represent different output views. Panel A reports Single's emitted-label hit@3, whereas Panel B reports HiED--DA's genuine ranked Top-3 Accuracy."
    )
    text = replace_once(text, old_panels, new_panels, "retrieval-panel explanation")

    retrieval_start = r"\begin{table}[H]
\centering
\caption{Retrieval-strategy results"
    text = replace_between(
        text,
        retrieval_start,
        r"\end{table}",
        RETRIEVAL_RESULTS_TABLE,
        "retrieval results table",
        include_end=True,
    )

    old_single_result = (
        "For Single, global Top-5 retrieval achieved the strongest values across the prespecified validation metrics available for selection and was therefore retained as the primary retrieval configuration. On the test split, it had the highest Top-1, Exact Match, Macro-F1, and Weighted-F1 values, whereas parent-balanced retrieval had the highest benchmark-defined emitted-label Top-3. Both retrieval configurations improved Top-1 over no retrieval, while the adjusted comparison between global and parent-balanced retrieval was statistically inconclusive."
    )
    new_single_result = (
        "For Single, global Top-5 retrieval achieved the strongest values across the prespecified validation metrics available for selection and was therefore retained as the primary retrieval configuration. On the test split, it had the highest Top-1, Exact Match, Macro-F1, and Weighted-F1 values, whereas parent-balanced retrieval had the highest emitted-label hit@3. Both retrieval configurations improved Top-1 over no retrieval, while the adjusted comparison between global and parent-balanced retrieval was statistically inconclusive."
    )
    text = replace_once(text, old_single_result, new_single_result, "Single retrieval-result paragraph")

    old_hied_result = (
        "For HiED--DA, the validation results were mixed. Global Top-5 achieved higher Top-1 Accuracy and Exact Match, whereas parent-balanced retrieval achieved higher genuine Top-3 Accuracy, Macro-F1, and Weighted-F1. Under the prespecified promotion rule, global Top-5 improved only two of the five selection metrics and therefore did not replace parent-balanced retrieval. Parent-balanced retrieval was consequently retained as the primary HiED--DA configuration."
    )
    new_hied_result = (
        "For HiED--DA, the validation results were mixed. Global Top-5 achieved higher Top-1 Accuracy and Exact Match, whereas parent-balanced retrieval achieved higher ranked Top-3 Accuracy, Macro-F1, and Weighted-F1. Under the prespecified promotion rule, global Top-5 improved only two of the five selection metrics and therefore did not replace parent-balanced retrieval. Parent-balanced retrieval was consequently retained as the primary HiED--DA configuration."
    )
    text = replace_once(text, old_hied_result, new_hied_result, "HiED retrieval-result paragraph")

    required = [
        r"\item The \emph{emitted-label sequence}, $E_3(x)$",
        r"\mathrm{Emitted\text{-}label\ hit@3}",
        r"\texttt{zero\_division=0}",
        r"\label{sec:metric-audit-boundary}",
        "0.177577",
        "864 cases and two diagnoses for 136 cases",
        "0.748$^{\\mathrm{E}}$",
        "0.802$^{\\mathrm{R}}$",
        "Split & Retrieval & Top-1 & Emitted hit@3",
        "Split & Retrieval & Top-1 & Ranked Top-3",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f"Missing required rewritten content: {missing}")

    forbidden = [
        "the same prompt-budget rule defined in Chapter~\\ref{ch:architecture}",
        "benchmark-defined emitted-label Top-3",
        "Single's benchmark-defined Top-3",
        "while their non-equivalent Top-3 measures are 0.748 and 0.802",
    ]
    remaining = [item for item in forbidden if item in text]
    if remaining:
        raise RuntimeError(f"Obsolete metric wording remains: {remaining}")

    if text.count(r"\newif\ifshowcomments") != before_guard:
        raise RuntimeError("The showcomments guard changed")
    if text.count(r"\showcommentstrue") + text.count(r"\showcommentsfalse") != before_showcomments:
        raise RuntimeError("The showcomments setting count changed")
    if text.count(r"\ct{") != before_ct or text.count(r"\wl{") != before_wl:
        raise RuntimeError("Advisor comment counts changed")

    target.write_text(text, encoding="utf-8")
    print(f"Updated {target}")
    print(f"Preserved advisor comments: CT={before_ct}, WL={before_wl}")


if __name__ == "__main__":
    main()
