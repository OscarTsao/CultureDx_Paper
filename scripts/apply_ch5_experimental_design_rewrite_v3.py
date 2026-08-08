from __future__ import annotations

from pathlib import Path


TARGET = Path("school/main.tex")


NEW_CHAPTER = r'''\chapter{Experimental Design}
\label{ch:experimental}

This chapter separates configuration selection, held-out evaluation, supporting sensitivity analyses, and clinician review. These parts use different populations and support different claims. Validation results select configurations; the internal held-out set provides the main internal estimate; MDD-5k tests synthetic cross-corpus transfer; and the psychiatrist study examines a small, selected synthetic disagreement sample.

\section{Study Sequence and Analysis Populations}
\label{sec:experimental-overview}

Table~\ref{tab:analysis-populations} summarizes the role of each analysis population. The case is the unit of analysis throughout. When a paired comparison is reported, both methods must cover the same case identifiers under the same metric definition.

\begin{table}[htbp]
\centering
\caption{Analysis populations and their roles in the study.}
\label{tab:analysis-populations}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.5cm}|>{\raggedright\arraybackslash}p{3.4cm}|X|}
\hline
\textbf{Analysis} & \textbf{Population} & \textbf{Role and claim boundary}\\
\hline
Retrieval-configuration selection (RQ3) & LingxiDiag public validation, $N=1000$ & Selects one retained retrieval configuration separately within Single and HiED; not treated as an independent performance estimate\\
\hline
Internal benchmark positioning (RQ1) & Fixed LingxiDiag internal held-out set, $N=1000$ & Main same-split comparison after configuration selection; complete architectures are compared descriptively\\
\hline
Recorded-output and primary-selection analyses (RQ2--RQ4) & Same internal $N=1000$; analyses using $I$ are restricted to 915 checker-eligible cases & Localizes disagreement among recorded output views and tests primary-selection policies under stated artifact and inference contracts\\
\hline
Sensitivity, scope, and transfer analyses (RQ5) & Internal $N=1000$; MDD-5k all cases $N=925$, in-scope cases $N=878$, and F32--F41 subset $N=490$ & Examines model scale and synthetic distribution shift; does not establish real-patient validity\\
\hline
Blinded psychiatrist annotation pilot & Twenty cases sampled from the 272-case $D_3=1$, $I=1$, $S=0$ group & Feasibility and exploratory agreement study on a selected synthetic sample; not a population-level clinical-accuracy estimate\\
\hline
\end{tabularx}
\end{table}

All computational analyses use synthetic Chinese psychiatric dialogue datasets. No real-patient transcript is included in the completed evaluation. Public-validation results are used for development decisions only, and held-out results are not used to revise the retained configurations.

\section{Configuration Selection and Internal Benchmark Positioning}
\label{sec:benchmark-retrieval-design}

\subsection{Compared Retrieval Configurations}

Retrieval is evaluated separately within the Single and HiED--DA architectures under three complete configurations: no retrieval, global Top-5 retrieval, and parent-balanced retrieval. Within an architecture, the backbone model, prompt family, configured diagnostic scope, decoding settings, and output contract remain fixed. Retrieved examples are supplied only to the diagnostic path; the Criterion Checkers continue to evaluate the current transcript without retrieved demonstrations, as defined in Chapter~\ref{ch:architecture}.

Global Top-5 and parent-balanced retrieval differ in demonstration count, composition, ordering, similarity distribution, label balance, and total prompt length. Their comparison therefore evaluates complete retrieval configurations rather than the isolated causal effect of parent balancing.

\subsection{Architecture-Specific Validation Decisions (RQ3)}

Single and HiED use separate validation-selection records. For Single, global Top-5 is the retained configuration. In the validation results, it has the highest Top-1 Accuracy, Exact Match, Macro-F1, and Weighted-F1 among the three Single configurations, while parent-balanced retrieval has the highest emitted-label hit@3. This is treated as an architecture-specific validation decision; the HiED promotion gate described below is not retroactively applied to Single.

For HiED--DA, parent-balanced retrieval is the initially retained configuration. Global Top-5 replaces it only when the validation bundle passes the required completeness, pairing, configuration, and regression gates and global Top-5 is strictly higher on all five headline validation measures: Top-1 Accuracy, genuine ranked Top-3 Accuracy, Exact Match, Macro-F1, and Weighted-F1. This is a conservative configuration-promotion rule rather than a statistical hypothesis test. Global Top-5 is higher on Top-1 Accuracy and Exact Match but lower on the other three measures, so it does not pass the all-five promotion condition and parent-balanced retrieval remains the primary HiED--DA configuration.

The architecture-specific three-label measures are used only within their corresponding selection records. Single uses emitted-label hit@3, whereas HiED uses genuine ranked Top-3 Accuracy. They are not treated as one common cross-architecture quantity. After selection, the retained configurations are frozen before internal held-out evaluation. The complete validation and held-out values are reported together in Chapter~\ref{ch:results} so that the post-selection rank reversal can be seen without changing the primary configurations.

\subsection{Same-Split Benchmark Positioning (RQ1)}

The validation-selected Single and HiED--DA configurations are evaluated together with the Majority baseline and TF--IDF with logistic regression on the same fixed 1,000-case internal held-out set. All rows use the parent-label projection and metric definitions in Chapter~\ref{ch:data}.

Committed Top-1 Accuracy is the primary common measure because every configuration produces one committed primary diagnosis. Genuine ranked Top-3 is available for TF--IDF with logistic regression and HiED, whereas emitted-label hit@3 is reported separately for Single and Majority. Exact Match and F1 evaluate each method's complete emitted label set. The different three-label views and output cardinalities are therefore identified explicitly rather than treated as interchangeable.

The Majority baseline predicts the most frequent scoring parent in the training source. TF--IDF with logistic regression follows the character-level one-vs-rest configuration reported in Appendix~\ref{app:supporting}. These comparisons are not component-controlled ablations: TF--IDF with logistic regression, Single, and HiED differ in training procedure, retrieval exposure, number of model calls, intermediate outputs, and output contract. Their performance differences describe complete configurations and cannot be attributed solely to multi-agent orchestration.

The current frozen snapshot contains a matching complete case-level output for the retained HiED--DA row but not for the complete headline rows of Majority, TF--IDF with logistic regression, or validation-selected Single Global Top-5. Accordingly, the RQ1 headline table is a same-split descriptive comparison. New paired confidence intervals, McNemar tests, prediction-overlap analyses, or output-cardinality claims are not inferred for contrasts involving those unmatched rows.

\section{Recorded-Output Disagreement Localization}
\label{sec:stage-wise-analysis-design}

RQ2 uses the case-level trace from the validation-selected parent-balanced HiED--DA configuration on the fixed 1,000-case internal held-out set. The trace records the genuine ranked differential, criterion states, criterion-compatible set, and committed primary diagnosis.

The analysis uses the indicators defined in Section~\ref{sec:case-level-indicators}: Top-3 candidate detection $D_3$, gold-label inclusion $I$, and committed-primary agreement $S$. $D_3$ and $S$ are available for all 1,000 cases. Analyses involving $I$ are restricted to the 915 checker-eligible cases whose benchmark gold-label set contains a non-\emph{Others} parent represented by a Criterion Checker.

For the checker-eligible analysis, cases are assigned to four mutually exclusive recorded-output groups according to Table~\ref{tab:disagreement-groups}. Assignment first separates committed-primary agreement from disagreement; disagreeing cases are then divided by candidate detection and gold-label inclusion. This is an analytical grouping order, not the chronological execution path of every finalization policy.

\begin{table}[H]
\centering
\caption{Mutually exclusive recorded-output groups used for RQ2.}
\label{tab:disagreement-groups}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}X|c|c|c|}
\hline
\textbf{Group} & $\boldsymbol{S}$ & $\boldsymbol{D_3}$ & $\boldsymbol{I}$ \\
\hline
Committed-primary agreement & 1 & 1 & -- \\
\hline
Top-3 candidate miss & 0 & 0 & -- \\
\hline
Gold label ranked but absent from the criterion-compatible set & 0 & 1 & 0 \\
\hline
Gold label ranked and criterion-compatible but not selected & 0 & 1 & 1 \\
\hline
\end{tabularx}
\parbox{0.96\textwidth}{\footnotesize
\textit{Note.} Under the DA ranking contract, $S=1$ implies $D_3=1$. A dash indicates that gold-label inclusion does not affect assignment to that group.
}
\end{table}

The fourth group is the strongest observable profile consistent with a primary-selection mismatch: a benchmark gold parent appears in both the genuine Top-3 and the criterion-compatible set but is not committed as primary. It does not by itself prove that the finalizer caused the disagreement. The ranking, criterion states, and committed diagnosis are connected model-derived outputs, and the criterion-compatible set is not a ranked primary-diagnosis recommendation.

\paragraph{Supplementary oracle analysis.}
\label{sec:oracle-design}
A gold-informed oracle estimates optimistic headroom within the prespecified recorded outputs. It searches the eligible ranked and criterion-compatible alternatives and selects a benchmark gold diagnosis whenever the oracle rules are satisfied, while leaving already matching cases unchanged. The procedure directly uses benchmark labels and assumes that all eligible disagreements can be corrected without creating new errors. It is therefore non-deployable and is reported only as an assumption-dependent upper-bound analysis. The candidate pool, eligibility thresholds, and sensitivity analyses are detailed in Appendix~\ref{app:supporting}.

\section{Primary-Selection Experiments}
\label{sec:primary-selection-intervention-design}

RQ4 asks whether an alternative method converts the available diagnostic artifacts into better committed-primary benchmark agreement than Direct-Answer (DA). The design separates fixed-artifact comparisons from complete reruns that introduce new model inference or repeated sampling.

\subsection{Primary Matched Finalization Comparison}

The prespecified primary comparison evaluates DA against Nominate-then-Select (NtS). Within each retrieval condition, both policies reuse the same Diagnostician ranking, criterion states, and criterion-compatible set. DA retains the Diagnostician's proposed primary diagnosis, whereas NtS applies the deterministic finalization rule defined in Chapter~\ref{ch:architecture}. NtS introduces no additional LLM inference.

DA and NtS are compared on the same 1,000 internal held-out cases under no retrieval, global Top-5 retrieval, and parent-balanced retrieval. The primary measure is the paired difference in committed Top-1 correctness. These three comparisons form one prespecified family and receive Holm adjustment. Paired-bootstrap confidence intervals and exact McNemar tests follow Chapter~\ref{ch:data}. Retrieval-by-finalization difference-in-differences contrasts are secondary analyses.

Because DA and NtS share the same upstream artifacts, their committed Top-1 comparison is the most controlled test of the two finalization policies. Exact Match, Macro-F1, and Weighted-F1 remain descriptive for this contrast because DA may additionally emit one comorbid diagnosis while NtS emits one diagnosis; differences in these set-based measures cannot be attributed to primary re-selection alone.

\subsection{Supporting Methods and Provenance Boundaries}

Table~\ref{tab:selection-method-provenance} groups the additional methods by the evidence needed to interpret them.

\begin{table}[htbp]
\centering
\caption{Provenance classes for supporting primary-selection analyses.}
\label{tab:selection-method-provenance}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.5cm}|>{\raggedright\arraybackslash}p{4.2cm}|X|}
\hline
\textbf{Evidence class} & \textbf{Methods} & \textbf{Interpretation boundary}\\
\hline
Fixed recorded artifacts & NtS; deterministic fusion; external forced-pairwise replay & Changes a deterministic decision rule on an available upstream trace; supports an isolated policy comparison only when the matched trace is retained\\
\hline
New-inference configurations & Independent pairwise comparison; two-view debate & Re-executes model-based stages and may change upstream outputs; evaluated as a complete configuration, not as an isolated finalizer ablation\\
\hline
Repeated-generation configurations & Self-consistency; confidence-informed self-consistency & Aggregates repeated Diagnostician samples under a larger sampling budget; does not reproduce the full fixed DA trace\\
\hline
\end{tabularx}
\end{table}

Deterministic fusion applies one validation-selected rule to the recorded ranking, compatibility status, and criterion-support summaries. Independent pairwise comparison and two-view debate introduce additional model calls. The retained internal pairwise result comes from a separate full-pipeline execution, so any difference from DA may include run-to-run changes in the ranking or other upstream outputs. Self-consistency and confidence-informed self-consistency aggregate repeated Diagnostician generations and are treated as sampling-based complete configurations.

Forced pairwise override is reported only in the external MDD-5k analysis, where it is a deterministic replay of retained pairwise preferences on a matched upstream trace. No internal forced-override result is reported because the archived internal artifacts do not establish a matched, separately executed forced-commit configuration for the former headline row.

Committed Top-1 Accuracy is the common RQ4 measure. A paired interval or McNemar test is reported only when both methods retain complete outputs for the same case identifiers. When only aggregate results remain, the comparison is descriptive. Detailed method rules, inference budgets, tie-breaking procedures, and retained paired statistics are reported in Appendix~\ref{app:supporting}.

\section{Sensitivity, Scope, and Transfer Analyses}
\label{sec:sensitivity-transfer-design}

RQ5 examines how the observed patterns change with model scale, synthetic corpus, configured diagnostic scope, and lexical transfer.

\paragraph{Within-family model-scale sensitivity.}
Qwen3-4B, 8B, 14B, and 32B are evaluated on the same fixed 1,000-case internal held-out set while holding the prompt family, configured diagnostic scope, retrieval policy, decoding contract, and evaluation metrics constant. Committed Top-1 Accuracy, genuine ranked Top-3 Accuracy, structured-output failures, and abstention events are recorded. This analysis is restricted to the evaluated Qwen3 family and serving setup.

\paragraph{External synthetic evaluation.}
MDD-5k is evaluated under a different Chinese synthetic dialogue-generation process. The main multi-class analysis uses all 925 patient-level cases and separately reports the 878 in-scope cases for which at least one benchmark gold diagnosis is represented in HiED's configured output space. All 878 in-scope cases are checker-eligible under the main profile and support the external $D_3$--$I$--$S$ analysis. A separate 490-case F32-versus-F41 subset is a secondary binary analysis rather than the main external estimate.

The external trace records the Diagnostician ranking, criterion states, criterion-compatible set, and committed primary diagnosis. It supports candidate detection, gold-label inclusion, committed-primary agreement, and matched policy replays on the same synthetic cases. A validated matched bundle for external retrieval-policy comparison is unavailable, so retrieval-policy transfer is not claimed.

\paragraph{Diagnostic-scope expansion.}
A configuration-level experiment expands the profile from 14 to 33 configured categories by adding category-specific checker definitions without changing model weights. This supporting analysis tests whether newly representable benchmark diagnoses enter the ranked candidates or become the committed primary diagnosis. It is evaluated separately from the primary 14-category external analysis.

\paragraph{Cross-corpus lexical transfer.}
The same TF--IDF classifier family is trained separately on each synthetic corpus and evaluated both within corpus and on the other corpus. This analysis tests whether lexical associations learned under one synthetic generation process transfer to the other; it does not repair the absence of real-patient validation.

\paragraph{Descriptive disagreement patterns.}
A first-listed-label confusion matrix, frequent reference-to-prediction pairs, and the $D_3$--$I$--$S$ profiles characterize the remaining disagreements. The first-listed label is used only to create a one-label visualization and is not substituted for the main multilabel evaluation.

The model-scale and MDD-5k analyses provide the main evidence for RQ5. Scope expansion, lexical transfer, and confusion-pattern analyses provide supporting evidence about the boundaries of the evaluated synthetic setting.

\section{Blinded Psychiatrist Annotation Pilot}
\label{sec:clinical-evaluation-plan}
\label{sec:lingxidiag-pilot-review}

The blinded annotation of 20 selected LingxiDiag cases is the only clinician-facing evaluation included in this thesis. It examines the feasibility of the review procedure and provides psychiatrist characterization of one selected synthetic disagreement population.

Twenty cases are sampled without replacement from the 272-case group satisfying $D_3=1$, $I=1$, and $S=0$. The random seed and case identifiers are fixed before review. Two psychiatrists independently review all cases in separately randomized orders. They remain blinded to the benchmark labels, HiED outputs, computational disagreement profile, case-selection rationale, and the other reviewer's responses.

Reviewers first read the transcript and record whether the available information supports a unique primary diagnosis, a provisional primary diagnosis, possible comorbid diagnoses, and up to three ranked differential diagnoses. They then label prespecified canonical evidence items and diagnosis-specific qualifiers as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. After the evidence annotation, they may revise their diagnostic judgments. Both provisional and final responses are retained.

Shared symptom and impairment concepts are annotated once, while diagnosis-specific duration, frequency, temporal, relational, threshold, and exclusion conditions remain separate. The mapping between the physician-facing evidence items and the original Criterion Checker items is frozen before annotation.

After both reviewers complete their independent final assessments, the research team compares their responses with the LingxiDiag benchmark labels, HiED ranked and committed diagnoses, criterion states, and system-derived compatibility decisions. Pre-consensus inter-rater agreement is calculated from the independent responses. Any later consensus or adjudication uses the transcript and independent annotations while the benchmark labels and HiED outputs remain concealed.

Planned analyses include final transcript-only primary-diagnosis agreement, ranked-differential coverage, criterion-state agreement, pre-consensus inter-rater agreement, provisional-to-final diagnostic changes, and agreement between psychiatrist-evidence-derived and system-derived compatibility decisions. Because the pilot contains only 20 synthetic cases selected from one disagreement group, it is interpreted as feasibility and exploratory agreement evidence rather than as an estimate of clinical accuracy or population prevalence.

'''


def replace_once(text: str, old: str, new: str, description: str) -> str:
    count = text.count(old)
    if count == 1:
        return text.replace(old, new, 1)
    if count == 0 and new in text:
        return text
    raise RuntimeError(f"Expected exactly one occurrence for {description}; found {count}")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    ct_before = text.count(r"\ct{")
    wl_before = text.count(r"\wl{")

    chapter_start = r"\chapter{Experimental Design}"
    chapter_end = r"\chapter{Internal Evaluation Results}"
    if NEW_CHAPTER not in text:
        if text.count(chapter_start) != 1 or text.count(chapter_end) != 1:
            raise RuntimeError("Could not identify the Chapter 5 replacement boundaries")
        start = text.index(chapter_start)
        end = text.index(chapter_end, start)
        text = text[:start] + NEW_CHAPTER + text[end:]

    old_tfidf = r'''The Top-1 difference between HiED--DA and TF--IDF is $-0.114$ (95\% CI [$-0.150$, $-0.079$]); the evaluated HiED configuration therefore does not provide an overall accuracy advantage on this benchmark.'''
    new_tfidf = r'''The aggregate Top-1 difference between HiED--DA and TF--IDF is $-0.114$. Because the frozen snapshot does not contain a TF--IDF case-level prediction file matching the complete headline row, no paired confidence interval or McNemar test is reported for this contrast. The evaluated HiED configuration therefore does not provide an overall accuracy advantage on this benchmark.'''
    text = replace_once(text, old_tfidf, new_tfidf, "TF--IDF comparison boundary")

    old_retrieval_results = r'''For Single, global Top-5 retrieval achieved the strongest values across the prespecified validation metrics available for selection and was therefore retained as the primary retrieval configuration. On the test split, it had the highest Top-1, Exact Match, Macro-F1, and Weighted-F1 values, whereas parent-balanced retrieval had the highest emitted-label hit@3. Both retrieval configurations improved Top-1 over no retrieval, while the adjusted comparison between global and parent-balanced retrieval was statistically inconclusive.

For HiED--DA, the validation results were mixed. Global Top-5 achieved higher Top-1 Accuracy and Exact Match, whereas parent-balanced retrieval achieved higher ranked Top-3 Accuracy, Macro-F1, and Weighted-F1. Under the prespecified promotion rule, global Top-5 improved only two of the five selection metrics and therefore did not replace parent-balanced retrieval. Parent-balanced retrieval was consequently retained as the primary HiED--DA configuration.

On the held-out test split, global Top-5 produced higher point estimates than parent-balanced retrieval across all five reported HiED metrics. This validation--test rank reversal is reported as a post-selection sensitivity result and does not revise the frozen primary configuration. The paired Top-1 contrasts were also statistically inconclusive.

Overall, retrieval provides a clearer benefit for the direct Single configuration than for HiED--DA. For HiED, the relative ordering of global and parent-balanced retrieval varies across validation metrics and held-out point estimates. Parent-balanced retrieval is the configuration retained by the predefined validation procedure.'''
    new_retrieval_results = r'''For Single, the archived validation-selection record retains global Top-5 retrieval. It has the highest validation Top-1 Accuracy, Exact Match, Macro-F1, and Weighted-F1, whereas parent-balanced retrieval has the highest emitted-label hit@3. On the held-out split, the same division remains: global Top-5 leads the four primary/set-based point estimates and parent-balanced leads emitted-label hit@3. This is an architecture-specific retained decision; the stricter HiED promotion gate is not applied to Single.

For HiED--DA, the validation results are mixed. Global Top-5 is higher on Top-1 Accuracy and Exact Match, whereas parent-balanced retrieval is higher on genuine ranked Top-3 Accuracy, Macro-F1, and Weighted-F1. The prespecified HiED gate promotes global Top-5 only after the required artifact and configuration checks pass and all five headline validation metrics strictly improve. Because only two metrics improve, global Top-5 does not replace parent-balanced retrieval.

On the held-out split, global Top-5 has higher point estimates than parent-balanced retrieval across all five HiED measures. This validation--test rank reversal is a post-selection sensitivity result and does not revise the frozen primary configuration.

Overall, retrieval provides a clearer held-out benefit for the direct Single configuration than for the retained HiED configuration. For HiED, the validation gate retains parent-balanced retrieval even though global Top-5 later has higher held-out point estimates. The held-out results are reported transparently but are not used to select a different primary configuration.'''
    text = replace_once(text, old_retrieval_results, new_retrieval_results, "Chapter 6 retrieval-selection interpretation")

    old_localization = r'''This pattern localizes the largest remaining difference among the recorded output views to committed-primary selection when a benchmark gold parent is already present in both the Top-3 and criterion-compatible set.'''
    new_localization = r'''This is the largest observed disagreement profile among the recorded output views. It is consistent with a committed-primary selection mismatch when a benchmark gold parent is already present in both the Top-3 and criterion-compatible set, but it does not identify the finalizer as the sole causal source of the disagreement.'''
    text = replace_once(text, old_localization, new_localization, "RQ2 causal boundary")

    forced_internal_row = r'''\hline
Forced pairwise override & 0.443 & $-0.075$ & [$-0.098$, $-0.053$] & Complete configuration\\
'''
    if forced_internal_row in text:
        text = text.replace(forced_internal_row, "", 1)

    old_internal_interpretation = r'''Deterministic fusion produces a slightly lower Top-1 point estimate than DA, but a paired case-level record was not retained for interval estimation. Forced pairwise override and two-view debate both reduce Top-1, with confidence intervals that exclude zero. Independent pairwise comparison produces a small positive point estimate, but its interval includes zero and therefore does not provide clear evidence of improvement.'''
    new_internal_interpretation = r'''Deterministic fusion produces a slightly lower Top-1 point estimate than DA, but a paired case-level record was not retained for interval estimation. Independent pairwise comparison produces a small positive point estimate, but its interval includes zero and therefore does not provide clear evidence of improvement. Because this pairwise result comes from a separate full-pipeline execution, it is not interpreted as an isolated finalizer effect. Two-view debate reduces Top-1, with a confidence interval that excludes zero. A forced-pairwise override row is not reported internally because the archived artifacts do not support the former value as a matched executed configuration; the available fixed-trace replay is reported only for MDD-5k.'''
    text = replace_once(text, old_internal_interpretation, new_internal_interpretation, "internal intervention provenance")

    old_forced_config = r'''Forced pairwise override & Full pairwise-commit pipeline with mandatory promotion of a valid in-cluster preference; genuine ranking may differ from DA & Complete-configuration sensitivity analysis, not an isolated finalizer or deployable fallback policy\\'''
    new_forced_config = r'''Forced pairwise override & External-only deterministic replay that promotes each valid preference already recorded by the MDD-5k pairwise trace to the committed primary & Fixed-trace policy replay; not a separately executed model configuration and not reported as an internal result\\'''
    text = replace_once(text, old_forced_config, new_forced_config, "appendix forced-pairwise provenance")

    old_pairwise_paragraph = r'''\paragraph{Pairwise configurations.}
Pairwise comparison begins with diagnoses whose criterion met ratio is at least 0.50. Candidates enter the close comparison cluster when the gap between adjacent met-ratio values is below 0.10. The pairwise Differential agent compares the eligible cluster, and a valid returned diagnosis is promoted according to the independent or forced-override contract. These runs use deterministic decoding (temperature 0, \texttt{top\_k}=1) and a 1,536-token output budget. Because the full HiED path is re-executed, the resulting ranking may differ from the recorded DA trace.'''
    new_pairwise_paragraph = r'''\paragraph{Pairwise configurations.}
Pairwise comparison begins with diagnoses whose criterion met ratio is at least 0.50. Candidates enter the close comparison cluster when the gap between adjacent met-ratio values is below 0.10. The pairwise Differential agent compares the eligible cluster. The independent pairwise analyses re-execute the HiED path with deterministic decoding (temperature 0, \texttt{top\_k}=1) and a 1,536-token output budget; their upstream ranking may therefore differ from the recorded DA trace. The forced-override result is different: it is an external-only deterministic replay that promotes valid preferences already stored in the matched MDD-5k pairwise trace. It introduces no new model call and is not a separately executed pipeline. No corresponding internal forced-override result is included.'''
    text = replace_once(text, old_pairwise_paragraph, new_pairwise_paragraph, "appendix pairwise interpretation")

    tfidf_paired_row = r'''\hline
TF--IDF + LR versus HiED--DA & 229 & 115 & $3.14\times10^{-9}$ & Holm-adjusted\\
'''
    if tfidf_paired_row in text:
        text = text.replace(tfidf_paired_row, "", 1)

    forced_paired_row = r'''\hline
DA versus forced pairwise override & 107 & 32 & $1.21\times10^{-10}$ & Exact\\
'''
    if forced_paired_row in text:
        text = text.replace(forced_paired_row, "", 1)

    old_external_group = r'''\multicolumn{4}{|c|}{\textbf{Additional-inference methods}}\\
\hline
Independent pairwise & Complete new-inference configuration & 57.08\% & $0.00$ (no committed changes)\\
\hline
Forced pairwise override & Deterministic replay of recorded pairwise preferences & 54.59\% & $-2.49$ [$-3.7$, $-1.3$]\\
\hline
Two-view debate & Complete new-inference configuration & 37.84\% & $-19.24$ [$-22.6$, $-16.0$]\\'''
    new_external_group = r'''\multicolumn{4}{|c|}{\textbf{Fixed-trace replay}}\\
\hline
Forced pairwise override & Deterministic replay of recorded pairwise preferences & 54.59\% & $-2.49$ [$-3.7$, $-1.3$]\\
\hline
\multicolumn{4}{|c|}{\textbf{New-inference methods}}\\
\hline
Independent pairwise & Complete new-inference configuration & 57.08\% & $0.00$ (no committed changes)\\
\hline
Two-view debate & Complete new-inference configuration & 37.84\% & $-19.24$ [$-22.6$, $-16.0$]\\'''
    text = replace_once(text, old_external_group, new_external_group, "external method provenance groups")

    old_external_heading = r'''\paragraph{Additional-inference methods.}

Independent pairwise reproduces the DA result exactly.'''
    new_external_heading = r'''\paragraph{Pairwise replay and new-inference methods.}

Independent pairwise reproduces the DA result exactly.'''
    text = replace_once(text, old_external_heading, new_external_heading, "external pairwise heading")

    if text.count(r"\ct{") != ct_before or text.count(r"\wl{") != wl_before:
        raise RuntimeError("Advisor-comment command counts changed")

    required = [
        r"\label{tab:analysis-populations}",
        "strictly higher on all five headline validation measures",
        "No internal forced-override result is reported",
        "no paired confidence interval or McNemar test is reported for this contrast",
        r"\label{tab:selection-method-provenance}",
    ]
    missing = [token for token in required if token not in text]
    if missing:
        raise RuntimeError(f"Missing required rewritten content: {missing}")

    forbidden = [
        "prespecified majority-based promotion rule",
        "Forced pairwise override & 0.443",
        "TF--IDF + LR versus HiED--DA & 229 & 115",
        "DA versus forced pairwise override & 107 & 32",
        "The Top-1 difference between HiED--DA and TF--IDF is $-0.114$ (95\\% CI",
    ]
    present = [token for token in forbidden if token in text]
    if present:
        raise RuntimeError(f"Obsolete or unsupported content remains: {present}")

    TARGET.write_text(text, encoding="utf-8")
    print(f"Updated {TARGET}")
    print(f"Preserved advisor comments: CT={ct_before}, WL={wl_before}")


if __name__ == "__main__":
    main()
