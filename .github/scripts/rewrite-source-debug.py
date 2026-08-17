from __future__ import annotations

import os
import re
from pathlib import Path

repo = os.environ.get("GITHUB_REPOSITORY", "")
if repo == "OscarTsao/CultureDx_Paper":
    thesis = Path("school/main.tex")
    figure_src = Path("figures/src/fig_pipeline_round20c_tikz.tex")
    figure_pdf = Path("figures/fig_pipeline_round20c.pdf")
elif repo == "OscarTsao/CultureDx":
    thesis = Path("paper/school/HiED_school_version.tex")
    figure_src = Path("paper/figures/src/fig_pipeline_round20c_tikz.tex")
    figure_pdf = Path("paper/figures/fig_pipeline_round20c.pdf")
else:
    raise SystemExit(f"Unsupported repository: {repo}")

text = thesis.read_text(encoding="utf-8")


def replace_block(source: str, start: str, end: str, replacement: str) -> str:
    if source.count(start) != 1:
        raise SystemExit(f"Start marker is not unique: {start!r} ({source.count(start)})")
    if source.count(end) != 1:
        raise SystemExit(f"End marker is not unique: {end!r} ({source.count(end)})")
    i = source.index(start)
    j = source.index(end, i)
    return source[:i] + replacement.rstrip() + "\n\n" + source[j:]


ch3_overview = r"""\section{Overview of HiED and Study Scope}
\label{sec:hied-overview}

Figure~\ref{fig:single-vs-hied-architecture} shows the HiED workflow. Every case begins with the same fixed psychiatric interview transcript. HiED then processes the transcript through two paths and combines their outputs when choosing the final primary diagnosis.

\subsection{Single LLM Baseline}
\label{sec:single-architecture}

The Single LLM baseline can be understood as using only the diagnosis path in Figure~\ref{fig:single-vs-hied-architecture}. It receives the transcript and optional similar cases, then returns the final diagnostic output. It does not provide the Top-3 diagnoses, criterion states, or criterion-compatible set used in the stage-wise analysis.

The Single LLM may return a primary diagnosis and an optional additional diagnosis. These are final outputs, not a standardized ranked differential diagnosis. The Single LLM is therefore used mainly as a direct final-diagnosis baseline.

\subsection{HiED Two-Path Architecture}
\label{sec:hied-two-path-architecture}

The upper path is the diagnosis path. The Similar-Case Retriever first finds related training examples. The Diagnostician then reads the current transcript and these examples. It produces the Top-3 diagnoses, proposes a primary diagnosis, and may add one comorbid diagnosis.

The lower path is the criterion-checking path. Diagnosis-specific Criterion Checkers read the same transcript and mark each criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_\allowbreak{}evidence}. The Compatibility Auditor applies the study rules and forms the criterion-compatible set.

The finalization step uses the diagnosis-path and criterion-path outputs to record one final primary diagnosis. Direct-Answer keeps the Diagnostician's proposed primary diagnosis. Nominate-then-Select instead chooses from the ranked diagnoses that pass the compatibility rules.

The two paths provide different views of the same transcript. They are not independent expert opinions, because both paths use the same input and may share model errors.

\begin{figure}[htbp]
\centering
\includegraphics[width=1.0\textwidth]{fig_pipeline_round20c.pdf}
\caption{HiED uses a diagnosis path and a criterion-checking path. The diagnosis path produces the Top-3 diagnoses and a proposed primary diagnosis. The criterion path produces criterion states and a criterion-compatible set. Finalization records the final primary diagnosis. The Single LLM baseline uses only the diagnosis path and reports the final diagnostic output.}
\label{fig:single-vs-hied-architecture}
\label{fig:pipeline-thesis-rewrite}
\end{figure}
\FloatBarrier

\subsection{Recorded Outputs}
\label{sec:recorded-output-differences}

HiED records five outputs for each case: the Top-3 diagnoses, the proposed primary diagnosis, the criterion states, the criterion-compatible set, and the final primary diagnosis. These outputs allow candidate formation, criterion checking, and primary-diagnosis selection to be evaluated separately. They are visible system outputs, not hidden model reasoning or clinician-validated evidence.
"""

metric_section = r"""\section{Prediction Views and Metrics}
\label{sec:prediction-metrics}

The study uses five main measures. Each measure answers a different question.

\begin{table}[H]
\centering
\caption{Main evaluation measures and the outputs they assess.}
\label{tab:metric-definitions}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.0cm}|>{\raggedright\arraybackslash}p{4.2cm}|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Measure} & \textbf{Output used} & \textbf{Question}\\
\hline
Top-1 Accuracy & Final primary diagnosis & Does the final primary diagnosis match any reference diagnosis?\\
\hline
Top-3 Accuracy & First three ranked diagnoses & Does any reference diagnosis appear in the Top-3?\\
\hline
Gold-label inclusion & Criterion-compatible set & Does the compatible set contain any reference diagnosis?\\
\hline
Exact Match & Complete final diagnosis set & Is the full predicted set exactly the same as the reference set?\\
\hline
Macro-F1 / Weighted-F1 & Complete final diagnosis set & How well are the diagnosis labels identified across classes?\\
\hline
\end{tabularx}
\end{table}

For case $x$, let $G(x)$ be the projected reference-label set, $p_1(x)$ the final primary diagnosis, $R_3(x)$ the first three distinct parent labels in a ranked output, $L(x)$ the criterion-compatible set, and $M(x)$ the complete final diagnosis set.

Top-3 Accuracy is reported only for methods that produce a ranked output. TF--IDF with logistic regression uses its three highest class scores, and HiED uses the Diagnostician ranking. The Single LLM and Majority baseline do not provide the same ranked output, so their Top-3 entries are shown as not applicable in the main comparison.

Because a case may contain more than one reference label, Top-1 and Top-3 count a case as correct when at least one reference label is found in the evaluated output. Exact Match is stricter: the complete predicted set must equal the complete reference set.

\[
\mathrm{Top\text{-}1\ Accuracy}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[p_1(x)\in G(x)],
\]
\[
\mathrm{Top\text{-}3\ Accuracy}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[R_3(x)\cap G(x)\neq\varnothing],
\]
\[
\mathrm{Exact\ Match}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[M(x)=G(x)].
\]

Let the scoring classes be
\[
\mathcal{Y}=\{\mathrm{F20},\mathrm{F31},\mathrm{F32},\mathrm{F39},\mathrm{F41},\mathrm{F42},\mathrm{F43},\mathrm{F45},\mathrm{F51},\mathrm{F98},\mathrm{Z71},\mathrm{Others}\}.
\]
For class $c\in\mathcal{Y}$, the one-vs-rest F1 score is
\[
\mathrm{F1}_c=
\begin{cases}
\dfrac{2\mathrm{TP}_c}{2\mathrm{TP}_c+\mathrm{FP}_c+\mathrm{FN}_c}, & 2\mathrm{TP}_c+\mathrm{FP}_c+\mathrm{FN}_c>0,\\[6pt]
0, & \text{otherwise}.
\end{cases}
\]
Macro-F1 gives every class the same weight. Weighted-F1 gives more weight to classes with more reference cases. Both use the complete final diagnosis set, so they are affected by the number of diagnoses a method returns.

\subsection{Metric Recalculation}
\label{sec:metric-audit-boundary}

The saved 1,000-case HiED--DA results were recalculated with the definitions above. The values were Top-1 0.518, Top-3 0.802, Exact Match 0.409, Macro-F1 0.178, and Weighted-F1 0.434, matching the reported results.

HiED--DA returned one diagnosis for 864 cases and two diagnoses for 136 cases. This confirms that Exact Match and F1 evaluate the complete diagnosis set rather than the primary diagnosis alone. Complete case-level predictions were not available for every baseline row, so new paired tests are reported only when matching case-level results were available.
"""

ch5 = r"""\chapter{Experimental Design}
\label{ch:experimental}

This chapter explains how the study settings were selected and how each research question was tested. All completed experiments use synthetic Chinese psychiatric transcripts. The proposed psychiatrist review at the end of the chapter was not completed and is not part of the thesis results.

\section{Study Data and Main Analyses}
\label{sec:experimental-overview}

Table~\ref{tab:analysis-populations} summarizes the three main evaluation populations.

\begin{table}[htbp]
\centering
\caption{Main datasets and their roles in the study.}
\label{tab:analysis-populations}
\small
\setlength{\arrayrulewidth}{0.6pt}
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.2cm}|>{\raggedright\arraybackslash}p{4.0cm}|X|}
\hline
\textbf{Analysis} & \textbf{Data} & \textbf{Purpose}\\
\hline
Retrieval selection & LingxiDiag validation set, $N=1000$ & Select the retrieval setting for Single and HiED before test results are examined\\
\hline
Internal evaluation & LingxiDiag held-out set, $N=1000$; $N=915$ for criterion analysis & Compare the methods and locate where diagnosis differences occur\\
\hline
External evaluation & MDD-5k, $N=925$; $N=878$ for criterion analysis & Test whether the same stage-wise analysis can be used on a second synthetic dataset\\
\hline
\end{tabularx}
\setlength{\arrayrulewidth}{0.4pt}
\end{table}

Additional analyses examine model size, common diagnosis differences, and TF--IDF transfer across the two datasets. No real-patient transcript is used.

\section{Retrieval Settings}
\label{sec:benchmark-retrieval-design}

Three retrieval settings are compared within each architecture: no retrieval, Global Top-5, and parent-balanced retrieval. Global Top-5 returns the five most similar training cases. Parent-balanced retrieval limits repeated examples from the same parent label so that more diagnosis categories can be shown.

The validation set is used to select one setting before the held-out set is evaluated. Single retains Global Top-5. HiED retains parent-balanced retrieval. The held-out results are reported for comparison but are not used to change these choices.

\section{Stage-Wise Disagreement Analysis}
\label{sec:stage-wise-analysis-design}

RQ2 uses three case-level indicators:

\begin{itemize}
    \item $D_3=1$ when a reference diagnosis appears in the Top-3;
    \item $I=1$ when a reference diagnosis appears in the criterion-compatible set; and
    \item $S=1$ when the final primary diagnosis matches a reference diagnosis.
\end{itemize}

Cases that can be checked by the criterion path are divided into four groups.

\begin{table}[H]
\centering
\caption{Four groups used in the stage-wise analysis.}
\label{tab:disagreement-groups}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}X|c|c|c|}
\hline
\textbf{Group} & $\boldsymbol{S}$ & $\boldsymbol{D_3}$ & $\boldsymbol{I}$\\
\hline
Final primary diagnosis matches & 1 & 1 & --\\
\hline
Reference diagnosis missing from the Top-3 & 0 & 0 & --\\
\hline
Reference diagnosis in the Top-3 but not in the compatible set & 0 & 1 & 0\\
\hline
Reference diagnosis in both views but not selected as primary & 0 & 1 & 1\\
\hline
\end{tabularx}
\parbox{0.96\textwidth}{\footnotesize A dash means that compatibility is not used to define that group.}
\end{table}

\paragraph{Gold-informed upper bound.}
\label{sec:oracle-design}
A separate analysis uses the reference labels to estimate the largest possible improvement within the saved candidate and compatibility outputs. Because this analysis directly uses the answers, it is only an upper bound and is not a usable selection method. Full rules are provided in Appendix~\ref{app:supporting}.

\section{Primary-Diagnosis Selection Methods}
\label{sec:primary-selection-intervention-design}

RQ4 compares Direct-Answer with several ways to select the final primary diagnosis. Table~\ref{tab:selection-methods-simple} gives the main idea of each method.

\begin{table}[htbp]
\centering
\caption{Primary-diagnosis selection methods.}
\label{tab:selection-methods-simple}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.8cm}|X|}
\hline
\textbf{Method} & \textbf{How the final primary diagnosis is chosen}\\
\hline
Direct-Answer (DA) & Keep the primary diagnosis proposed by the Diagnostician\\
\hline
Nominate-then-Select (NtS) & Choose the highest-ranked diagnosis that is also in the criterion-compatible set\\
\hline
Deterministic fusion & Choose among eligible candidates using the criterion \textit{met ratio}; ranking is used when needed\\
\hline
Pairwise comparison & Ask an additional LLM to compare close candidates and select the stronger diagnosis\\
\hline
Two-view debate & One advocate represents the diagnosis path and one represents the criterion path; after their debate, a judge agent selects the final diagnosis\\
\hline
Self-consistency & Run the Diagnostician $K$ times, with $K=3$ or $5$, and use majority voting\\
\hline
Confidence-informed self-consistency & Use the same repeated Diagnostician outputs, but weight each vote by the reported confidence\\
\hline
\end{tabularx}
\end{table}

DA and NtS use the same Top-3 and criterion results, so their Top-1 difference directly reflects the final selection rule. The other methods add model calls or repeated generation. Their results therefore compare complete methods rather than one isolated step. Exact thresholds and tie rules are kept in Appendix~\ref{app:supporting}.

\section{External Evaluation and Supporting Analyses}
\label{sec:sensitivity-transfer-design}

RQ5 applies the same Top-3, compatibility, and final-primary measures to MDD-5k. The main result uses all 925 cases for Top-1 and Top-3, and the 878 checker-eligible cases for the stage-wise analysis.

The study also tests the TF--IDF classifier across the two datasets and compares Qwen3 model sizes. These are supporting analyses. They do not establish performance on real psychiatric consultations.

\section{Proposed Psychiatrist Review}
\label{sec:clinical-evaluation-plan}
\label{sec:lingxidiag-pilot-review}

This review was not completed within the thesis period. It is included only as a plan for future work and provides no clinician result in this thesis.

Twenty cases will be sampled from the 272 cases in which a reference diagnosis appears in both the Top-3 and the criterion-compatible set but is not selected as the final primary diagnosis. One psychiatrist will first review the transcripts without seeing the dataset labels or HiED outputs.

For each case, the psychiatrist will state whether the transcript supports a clear primary diagnosis, a provisional diagnosis, or no unique diagnosis. The psychiatrist will then record one primary diagnosis, up to three differential diagnoses, possible comorbidity, confidence, and missing information.

After this first assessment is locked, the dataset label will be shown. The psychiatrist will judge whether it matches the primary diagnosis, is a reasonable differential or comorbid diagnosis, is not supported, or cannot be judged because information is missing.

Because the review uses one psychiatrist and twenty selected synthetic cases, it can provide only a preliminary check of label alignment. It cannot establish dataset-wide validity or clinical accuracy.
"""

ch6 = r"""\chapter{Internal Evaluation Results}
\label{ch:results}

This chapter reports the internal results for the fixed LingxiDiag held-out set. It first shows retrieval selection, then compares the main methods, locates the stage of disagreement, and tests alternative primary-diagnosis selection methods.

\section{Retrieval Results}
\label{sec:retrieval-results}

Table~\ref{tab:retrieval-results} reports validation and held-out results for the three retrieval settings. A dagger marks the setting selected on validation.

\begin{table}[H]
\centering
\caption{Retrieval results for Single and HiED--DA.}
\label{tab:retrieval-results}
\small

\textbf{Panel A. Single}
\vspace{0.3em}
\begin{adjustbox}{max width=\textwidth}
\begin{tabular}{|l|l|c|c|c|c|}
\hline
Split & Retrieval & Top-1 & Exact Match & Macro-F1 & Weighted-F1\\
\hline
Validation & None & 0.466 & 0.016 & 0.174 & 0.429\\
Validation & Global Top-5$^{\dagger}$ & 0.519 & 0.030 & 0.209 & 0.456\\
Validation & Parent-balanced & 0.507 & 0.016 & 0.195 & 0.437\\
\hline
Held-out & None & 0.466 & 0.017 & 0.183 & 0.426\\
Held-out & Global Top-5$^{\dagger}$ & 0.517 & 0.029 & 0.224 & 0.447\\
Held-out & Parent-balanced & 0.508 & 0.011 & 0.192 & 0.433\\
\hline
\end{tabular}
\end{adjustbox}

\vspace{0.8em}
\textbf{Panel B. HiED--DA}
\vspace{0.3em}
\begin{adjustbox}{max width=\textwidth}
\begin{tabular}{|l|l|c|c|c|c|c|}
\hline
Split & Retrieval & Top-1 & Top-3 & Exact Match & Macro-F1 & Weighted-F1\\
\hline
Validation & None & 0.509 & 0.792 & 0.456 & 0.173 & 0.428\\
Validation & Global Top-5 & 0.525 & 0.797 & 0.432 & 0.178 & 0.435\\
Validation & Parent-balanced$^{\dagger}$ & 0.523 & 0.800 & 0.428 & 0.181 & 0.440\\
\hline
Held-out & None & 0.510 & 0.786 & 0.404 & 0.174 & 0.437\\
Held-out & Global Top-5 & 0.524 & 0.815 & 0.435 & 0.196 & 0.437\\
Held-out & Parent-balanced$^{\dagger}$ & 0.518 & 0.802 & 0.409 & 0.178 & 0.434\\
\hline
\end{tabular}
\end{adjustbox}
\end{table}

Global Top-5 was selected for Single and increased held-out Top-1 from 0.466 to 0.517. Parent-balanced retrieval was selected for HiED on validation. Global Top-5 later had slightly higher held-out values, but the test set was not used to change the selected setting.

\paragraph{Answer to RQ3.}
Retrieval gives higher Top-1 point estimates for Single. The differences among the three HiED settings are smaller and depend on the split and measure.

\section{Main Internal Performance}
\label{sec:validation-retrieval-selection}
\label{sec:matched-baselines-retrieval}

Table~\ref{tab:matched-baselines-retrieval} compares the selected methods on the same 1,000-case held-out set.

\begin{table}[H]
\centering
\caption{Main internal comparison on the 1,000-case LingxiDiag held-out set.}
\label{tab:matched-baselines-retrieval}
\small
\begin{adjustbox}{max width=\textwidth}
\begin{tabular}{|l|l|c|c|c|c|c|}
\hline
System & Retrieval & Top-1 & Top-3 & Exact Match & Macro-F1 & Weighted-F1\\
\hline
Majority & None & 0.398 & --- & 0.327 & 0.047 & 0.207\\
\hline
TF--IDF + LR & None & 0.632 & 0.923 & 0.321 & 0.393 & 0.601\\
\hline
Single & Global Top-5 & 0.517 & --- & 0.029 & 0.224 & 0.447\\
\hline
HiED--DA & Parent-balanced & 0.518 & 0.802 & 0.409 & 0.178 & 0.434\\
\hline
\end{tabular}
\end{adjustbox}
\parbox{0.96\textwidth}{\footnotesize Top-3 is shown only for methods with a ranked output.}
\end{table}

TF--IDF with logistic regression has the highest same-source Top-1, Top-3, Macro-F1, and Weighted-F1. Single and HiED have almost the same Top-1 result. HiED does not show an overall accuracy advantage; its added value is the Top-3 and criterion information used in the analyses below.

\paragraph{Answer to RQ1.}
TF--IDF with logistic regression is the strongest same-source classifier in this comparison. HiED and Single have almost identical Top-1 results.

\section{Stage-Wise Disagreement Results}
\label{sec:stage-wise-disagreement-results}

Figure~\ref{fig:selection-bottleneck} compares Top-1 and Top-3 for HiED. A reference diagnosis appears in the Top-3 in 802 cases, while the final primary diagnosis matches in 518 cases.

\begin{figure}[H]
\centering
\includegraphics[width=0.98\textwidth]{fig_b_selection_bottleneck.pdf}
\caption{HiED Top-1 and Top-3 results on the 1,000-case internal held-out set.}
\label{fig:selection-bottleneck}
\end{figure}

Among the 915 checker-eligible cases, a reference diagnosis appears in the criterion-compatible set in 857 cases (93.7\%). The median compatible set contains six of the fourteen configured diagnoses. The criterion path therefore keeps most reference diagnoses but often keeps several alternatives at the same time.

Table~\ref{tab:d3rs-joint} shows the four main groups.

\begin{table}[htbp]
\centering
\caption{Stage-wise results for the 915 checker-eligible cases.}
\label{tab:d3rs-joint}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}X|r|r|}
\hline
\textbf{Group} & \textbf{Cases} & \textbf{Share}\\
\hline
Final primary diagnosis matches & 518 & 56.6\%\\
\hline
Reference diagnosis missing from the Top-3 & 113 & 12.3\%\\
\hline
Reference diagnosis in the Top-3 but not in the compatible set & 12 & 1.3\%\\
\hline
Reference diagnosis in both views but not selected as primary & 272 & 29.7\%\\
\hline
\end{tabularx}
\end{table}

The largest disagreement group contains 272 cases. In these cases, a reference diagnosis is already present in both the Top-3 and the compatible set, but another diagnosis is selected as primary. This does not prove that the finalization step alone caused the difference. It shows where the difference is visible in the saved outputs.

The full six-profile table and the gold-informed upper-bound analysis are reported in Appendix~\ref{app:supporting}.

\paragraph{Answer to RQ2.}
Differences occur at more than one stage, but the largest group appears after the reference diagnosis is already present in the Top-3 and the compatible set.

\section{Primary-Diagnosis Selection Results}
\label{sec:nts-factorial}
\label{sec:additional-selection-results}

Table~\ref{tab:nts-factorial} compares DA and NtS when both use the same earlier HiED outputs.

\begin{table}[htbp]
\centering
\caption{Top-1 comparison of DA and NtS on the internal held-out set.}
\label{tab:nts-factorial}
\small
\begin{tabular}{|l|c|c|c|}
\hline
Retrieval & DA Top-1 & NtS Top-1 & Difference, pp (95\% CI)\\
\hline
None & 51.0\% & 48.2\% & $-2.8$ [$-4.1$, $-1.5$]\\
\hline
Global Top-5 & 52.4\% & 49.5\% & $-2.9$ [$-4.4$, $-1.4$]\\
\hline
Parent-balanced & 51.8\% & 49.0\% & $-2.8$ [$-4.3$, $-1.3$]\\
\hline
\end{tabular}
\end{table}

NtS lowers Top-1 by about 2.8--2.9 percentage points in all three retrieval settings. A compatibility-first rule can replace correct DA choices because many diagnoses pass the compatibility rules.

Table~\ref{tab:internal-selection-results} summarizes the other internal methods.

\begin{table}[htbp]
\centering
\caption{Other primary-diagnosis selection methods on the internal held-out set.}
\label{tab:internal-selection-results}
\small
\begin{tabular}{|l|c|c|}
\hline
Method & Top-1 & Difference vs DA (95\% CI)\\
\hline
DA & 0.518 & ---\\
\hline
Deterministic fusion & 0.514 & $-0.004$ (paired interval unavailable)\\
\hline
Pairwise comparison & 0.524 & $+0.006$ [$-0.010$, 0.022]\\
\hline
Two-view debate & 0.485 & $-0.033$ [$-0.049$, $-0.018$]\\
\hline
\end{tabular}
\end{table}

Deterministic fusion is slightly below DA. The small pairwise increase is uncertain because its confidence interval includes zero. Debate performs below DA. Repeated-generation results also do not show a clear improvement and are listed in Appendix~\ref{app:supporting}.

\paragraph{Answer to RQ4.}
None of the tested selection methods gives a clear and reliable improvement over DA.

\section{Supporting Internal Analyses}
\label{sec:model-scale-disagreement}

\paragraph{Model size.}
\ThesisFigure{fig_a_size_robustness.pdf}{Top-1 results across the tested Qwen3 model sizes. The shaded bands show the observed range, not confidence intervals.}{fig:size-robustness}

Single improves as model size increases. HiED varies less across the tested sizes, while its Top-3 Accuracy remains between 0.803 and 0.818. These results apply only to the tested Qwen3 models.

\paragraph{Common diagnosis differences.}
\ThesisFigure{fig_d_confusion_heatmap.pdf}{First-listed-label confusion matrix for the internal held-out set.}{fig:confusion-thesis-rewrite}

The most common direction is F41 to F32. This figure uses one first-listed reference label per case and is descriptive; the main evaluation uses the full reference-label set.

\section{Chapter Summary}

The internal results support four main conclusions. Retrieval helps Single more than HiED. TF--IDF with logistic regression is the strongest same-source classifier. The largest HiED disagreement group appears when a reference diagnosis is already in both the Top-3 and the compatible set. None of the tested primary-diagnosis selection methods clearly improves on DA.
"""

ch7 = r"""\chapter{External Synthetic Evaluation}
\label{ch:external}

This chapter tests whether the same stage-wise analysis can be used on MDD-5k, a second synthetic Chinese psychiatric dialogue dataset. The results do not represent real-patient clinical validation.

\section{External Data}
\label{sec:external-populations}

Table~\ref{tab:external-inventory} shows the two populations used in the chapter.

\begin{table}[htbp]
\centering
\caption{MDD-5k populations used in the external evaluation.}
\label{tab:external-inventory}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{4.0cm}|c|X|}
\hline
\textbf{Population} & \textbf{Cases} & \textbf{Use}\\
\hline
All MDD-5k cases & 925 & Top-1, Top-3, and method comparison\\
\hline
Checker-eligible cases & 878 & Criterion inclusion and stage-wise analysis\\
\hline
\end{tabularx}
\end{table}

\section{Main External Results}
\label{sec:external-main-performance}

Table~\ref{tab:external-summary-rewrite} compares the internal HiED result with MDD-5k. The rows come from different synthetic datasets and are not paired.

\begin{table}[htbp]
\centering
\caption{Internal and external HiED results.}
\label{tab:external-summary-rewrite}
\small
\begin{tabular}{|l|c|c|c|c|}
\hline
Population & Cases & Top-1 & Top-3 & Gold in compatible set\\
\hline
LingxiDiag internal & 1,000 & 0.518 & 0.802 & 0.937$^{*}$\\
\hline
MDD-5k, all cases & 925 & 0.571 & 0.851 & ---\\
\hline
MDD-5k, checker-eligible & 878 & 0.601 & 0.896 & 0.786\\
\hline
\end{tabular}
\parbox{0.96\textwidth}{\footnotesize $^{*}$The internal compatibility value uses the 915 checker-eligible LingxiDiag cases.}
\end{table}

On all 925 MDD-5k cases, HiED reaches 0.571 Top-1 and 0.851 Top-3. On the 878 checker-eligible cases, the compatible set contains a reference diagnosis in 78.6\% of cases. The median compatible set size is six.

The exact rates differ from LingxiDiag, but the three output views remain distinct: a diagnosis can appear in the Top-3, pass the compatibility rules, and still not be selected as the final primary diagnosis.

\section{External Stage-Wise Results}
\label{sec:external-stagewise}

Table~\ref{tab:external-disagreement-profiles} applies the same four groups used in the internal analysis.

\begin{table}[htbp]
\centering
\caption{Stage-wise results for the 878 checker-eligible MDD-5k cases.}
\label{tab:external-disagreement-profiles}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}X|r|r|}
\hline
\textbf{Group} & \textbf{Cases} & \textbf{Share}\\
\hline
Final primary diagnosis matches & 528 & 60.1\%\\
\hline
Reference diagnosis missing from the Top-3 & 91 & 10.4\%\\
\hline
Reference diagnosis in the Top-3 but not in the compatible set & 34 & 3.9\%\\
\hline
Reference diagnosis in both views but not selected as primary & 225 & 25.6\%\\
\hline
\end{tabularx}
\end{table}

The largest disagreement group again occurs when a reference diagnosis is already present in the Top-3 and the compatible set. This supports using the same stage-wise analysis on a second synthetic dataset. It does not prove that the finalization step alone caused the differences.

\section{External Primary-Diagnosis Selection Results}
\label{sec:mdd-multiway}

Table~\ref{tab:mdd-finalization-results} compares the main selection methods. The method descriptions are given in Chapter~\ref{ch:experimental}, so the table keeps only the result columns.

\begin{table}[htbp]
\centering
\caption{Primary-diagnosis selection results on the 925 MDD-5k cases.}
\label{tab:mdd-finalization-results}
\small
\begin{tabular}{|l|c|c|}
\hline
Method & Top-1 & Difference vs DA, pp (95\% CI)\\
\hline
Direct-Answer & 57.08\% & ---\\
\hline
Nominate-then-Select & 40.65\% & $-16.43$ [$-19.5$, $-13.5$]\\
\hline
Deterministic fusion & 47.14\% & $-9.95$ [$-12.4$, $-7.5$]\\
\hline
Pairwise comparison & 57.08\% & $0.00$ [0.0, 0.0]\\
\hline
Two-view debate & 37.84\% & $-19.24$ [$-22.1$, $-16.4$]\\
\hline
Self-consistency, $K=3$ & 57.84\% & $+0.76$ [$-0.5$, 2.1]\\
\hline
Self-consistency, $K=5$ & 58.16\% & $+1.08$ [$-0.1$, 2.4]\\
\hline
\end{tabular}
\end{table}

NtS, deterministic fusion, and debate reduce Top-1. Pairwise comparison does not change Top-1. Self-consistency has small positive point estimates, but both confidence intervals include zero. No method gives a clear external improvement over DA.

Detailed paired counts and the additional confidence-weighted results are reported in Appendix~\ref{app:supporting}.

\section{TF--IDF Transfer Across Datasets}
\label{sec:external-lexical-transfer}

Table~\ref{tab:lexical-transfer-rewrite} tests whether the TF--IDF classifier transfers between LingxiDiag and MDD-5k.

\begin{table}[htbp]
\centering
\caption{TF--IDF with logistic regression within and across the two synthetic datasets.}
\label{tab:lexical-transfer-rewrite}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.3cm}|>{\raggedright\arraybackslash}p{3.3cm}|c|c|c|}
\hline
Training source & Evaluation source & Cases & Top-1 & Top-3\\
\hline
LingxiDiag-16K & LingxiDiag held-out & 1,000 & 0.602 & 0.935\\
\hline
LingxiDiag-16K & MDD-5k & 925 & 0.059 & 0.613\\
\hline
MDD-5k training split & MDD-5k held-out split & 185 & 0.632 & 0.842\\
\hline
MDD-5k training split & LingxiDiag held-out & 1,000 & 0.476 & 0.676\\
\hline
\end{tabularx}
\end{table}

TF--IDF performs much better when training and evaluation use the same dataset. Performance falls in both transfer directions, especially from LingxiDiag to MDD-5k. This shows that the strong same-source result depends heavily on dataset-specific wording and label patterns. It does not prove that HiED generalizes better.

\section{Answer to RQ5 and Chapter Summary}

The same stage-wise analysis can be applied to MDD-5k. The largest external disagreement group, like the largest internal group, contains cases in which a reference diagnosis is already in the Top-3 and compatible set but is not selected as primary. However, the exact rates differ between the two datasets. The external selection methods also fail to show a clear improvement over DA, and TF--IDF shows strong source dependence.
"""

text = replace_block(text, r"\section{Overview of HiED and Study Scope}", r"\section{Diagnosis Path: Candidate Formation and Primary Proposal}", ch3_overview)
text = replace_block(text, r"\section{Prediction Views and Metrics}", r"\section{Case-Level Indicators for Disagreement Localization}", metric_section)
text = replace_block(text, r"\chapter{Experimental Design}", r"\chapter{Internal Evaluation Results}", ch5)
text = replace_block(text, r"\chapter{Internal Evaluation Results}", r"\chapter{External Synthetic Evaluation}", ch6)
text = replace_block(text, r"\chapter{External Synthetic Evaluation}", r"\chapter{Characterization of Recorded-Output Disagreements}", ch7)

# Keep the new simple metric-table label consistent.
text = text.replace("tab:metric-contract", "tab:metric-definitions")

# Unify Top-3 wording in the remaining chapters and appendices.
replacements = {
    "genuine ranked Top-3 Accuracy": "Top-3 Accuracy",
    "genuine Top-3 Accuracy": "Top-3 Accuracy",
    "ranked Top-3 Accuracy": "Top-3 Accuracy",
    "Ranked Top-3 Accuracy": "Top-3 Accuracy",
    "genuine ranked Top-3": "Top-3",
    "genuine Top-3": "Top-3",
    "ranked Top-3": "Top-3",
    "Ranked Top-3": "Top-3",
    "Top-3 coverage": "Top-3 Accuracy",
    "candidate coverage": "Top-3 Accuracy",
    "benchmark-reference diagnosis": "reference diagnosis",
    "benchmark-reference parent": "reference parent",
    "benchmark gold parent": "reference parent",
    "benchmark gold diagnosis": "reference diagnosis",
    "committed primary diagnosis": "final primary diagnosis",
    "committed primary": "final primary",
    "committed-primary agreement": "final-primary agreement",
    "primary-commitment disagreement": "primary-selection disagreement",
    "primary commitment": "primary-diagnosis selection",
    "output contracts": "output formats",
    "output contract": "output format",
    "evaluation contracts": "evaluation rules",
    "evaluation contract": "evaluation framework",
    "metric contracts": "metric definitions",
    "metric contract": "metric definition",
    "scoring contracts": "scoring rules",
    "scoring contract": "scoring rule",
    "ranking contracts": "ranking rules",
    "ranking contract": "ranking rule",
    "inference contracts": "inference settings",
    "inference contract": "inference setting",
    "evidence contracts": "information used for comparison",
    "evidence contract": "information used for comparison",
    "parent-label contracts": "parent-label mappings",
    "parent-label contract": "parent-label mapping",
    "study contracts": "study design",
    "study contract": "study design",
    "zero_division=0 contract": "zero_division=0 setting",
    "same-case stage-wise output and evaluation contract": "stage-wise evaluation framework that records the same outputs for every case",
    "stage-wise and inspectable output contract": "stage-wise and inspectable output framework",
    "stage-wise output and evaluation contract": "stage-wise evaluation framework",
    "archived trace lineages": "saved runs",
    "trace lineages": "saved runs",
    "trace lineage": "saved run",
    "recorded output lineage": "saved result version",
    "result lineages": "saved result versions",
    "lineages": "runs",
    "lineage": "run",
    "frozen snapshot": "saved results",
    "frozen repository snapshot": "saved repository results",
    "frozen configuration": "selected configuration",
    "frozen configurations": "selected configurations",
    "frozen trace": "saved case-level results",
    "matched trace": "matched case-level results",
    "external trace": "external case-level results",
    "internal trace": "internal case-level results",
    "upstream trace": "earlier outputs",
    "recorded artifacts": "recorded outputs",
    "additional recorded artifacts": "additional recorded outputs",
    "source artifact": "source file",
    "transfer artifact": "transfer results",
    "artifacts": "outputs",
    "artifact": "output",
    "provenance": "source information",
    "posthoc": "additional",
    "headroom": "room for improvement",
    "同病例的分階段輸出與評估契約": "能在同一病例中分開記錄與評估各階段輸出的框架",
    "評估契約": "評估框架",
    "輸出契約": "輸出格式",
    "internal HiED trace": "internal HiED case-level results",
    "model trace": "model output",
    "internal held-out trace": "internal held-out results",
    "same frozen internal trace": "same saved internal results",
    "frozen internal trace": "saved internal results",
    "case-level trace": "case-level results",
    "saved trace": "saved results",
    "result trace": "saved result",
    "result traces": "saved results",
    "output trace": "output record",
}
for old, new in replacements.items():
    text = text.replace(old, new)

# Remove remaining engineering wording where a direct sentence is clearer.
text = text.replace(
    "same-case stage-wise output and evaluation framework",
    "stage-wise evaluation framework that records the same outputs for every case",
)
text = text.replace(
    "The answers below apply only to the tested synthetic datasets, label mappings, output formats, and preserved result traces.",
    "The answers below apply only to the tested synthetic datasets, label mappings, and saved results.",
)
text = text.replace(
    "Reproduction requires the full evaluation framework: data split, model and prompt, retrieval configuration, diagnostic scope, saved result version, label projection, eligible population, output-view definition, and statistical procedure.",
    "Reproduction requires the same data split, model, prompt, retrieval setting, diagnostic scope, label mapping, eligible cases, metric definitions, and statistical procedure.",
)
text = text.replace(
    "A similar number obtained with a different Top-3 definition, denominator, saved run, or compatibility rule is not the same result.",
    "A similar number is not the same result when the Top-3 definition, denominator, saved run, or compatibility rule is different.",
)

# Remove obsolete visible phrases that should no longer appear.
forbidden_visible = [
    "emitted-label hit@3",
    "Emitted hit@3",
    "genuine Top-3",
    "genuine ranked Top-3",
    "Trace-Lineage",
    "trace lineage",
    "Posthoc fixed-trace forced-commit sweep",
    "Evidence contract",
    "evidence contract",
    "output contract",
    "evaluation contract",
    "metric contract",
    "scoring contract",
    "ranking contract",
    "inference contract",
    "parent-label contract",
]

# Some appendix text may still use the old Single three-label term. Replace it with a plain description.
text = re.sub(r"emitted-label hit@3", "Top-3 from final labels", text, flags=re.IGNORECASE)
text = text.replace("Top-3 from final labels", "final-label Top-3")

# Fix awkward terms produced by broad replacements.
text = text.replace("saved result versionss", "saved result versions")
text = text.replace("output completeness", "saved-result completeness")
text = text.replace("saved outputs completeness", "saved-result completeness")
text = text.replace("output and inference settings", "saved outputs and inference settings")

# Update the figure source. The workflow compiles this file into the PDF used as Figure 3.1.
figure_text = r"""\documentclass[tikz,border=4pt]{standalone}
\usepackage{fontspec}
\usepackage{xeCJK}
\setmainfont{Liberation Serif}
\setCJKmainfont{Noto Serif CJK TC}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta,calc}

\definecolor{bggray}{RGB}{246,247,248}
\definecolor{lanefill}{RGB}{240,242,244}
\definecolor{laneBlue}{RGB}{38,79,135}
\definecolor{iofill}{RGB}{234,248,244}
\definecolor{iodraw}{RGB}{0,117,89}
\definecolor{llmfill}{RGB}{252,244,226}
\definecolor{llmdraw}{RGB}{190,119,16}
\definecolor{detfill}{RGB}{244,238,252}
\definecolor{detdraw}{RGB}{126,75,183}
\definecolor{outfill}{RGB}{252,252,251}
\definecolor{outdraw}{RGB}{104,111,116}
\definecolor{textgray}{RGB}{54,60,66}

\newcommand{\ModuleTitle}[1]{{\bfseries\fontsize{13.2}{14.6}\selectfont #1}}
\newcommand{\ModuleSub}[1]{{\fontsize{9.8}{11.1}\selectfont #1}}
\newcommand{\OutputTitle}[1]{{\bfseries\fontsize{11.2}{12.6}\selectfont #1}}
\newcommand{\OutputSub}[1]{{\fontsize{9.2}{10.5}\selectfont #1}}
\newcommand{\LegendText}[1]{{\fontsize{9.2}{10.4}\selectfont #1}}
\newcommand{\LaneLabel}[1]{{\bfseries\fontsize{14.5}{16.0}\selectfont #1}}

\begin{document}
\begin{tikzpicture}[
  font=\rmfamily,
  >={Latex[length=2.3mm]},
  mainarrow/.style={draw=black, line width=0.82pt, -{Latex[length=2.45mm]}},
  module/.style={line width=1.0pt, minimum height=1.42cm, align=center, inner sep=5pt},
  llm/.style={module, rounded corners=4pt, draw=llmdraw, fill=llmfill, text=textgray},
  deterministic/.style={module, rounded corners=4pt, draw=detdraw, fill=detfill, text=textgray, line width=1.1pt},
  io/.style={module, rounded corners=6pt, draw=iodraw, fill=iofill, text=textgray, line width=1.15pt},
  outputbox/.style={rounded corners=5pt, draw=outdraw, fill=outfill, dashed, line width=0.8pt, minimum height=1.28cm, align=center, inner sep=4pt},
  finalout/.style={rounded corners=5pt, draw=iodraw, fill=iofill, line width=1.1pt, minimum height=1.28cm, align=center, inner sep=4pt},
  inputlabel/.style={font=\fontsize{9.5}{10.8}\selectfont, text=llmdraw},
  legendswatch/.style={rectangle, minimum width=0.40cm, minimum height=0.23cm, inner sep=0pt, line width=0.8pt}
]

\fill[bggray] (-0.35,-5.63) rectangle (21.72,4.45);
\fill[lanefill, rounded corners=6pt] (3.07,1.91) rectangle (18.05,4.17);
\fill[lanefill, rounded corners=6pt] (3.07,-4.15) rectangle (18.45,-1.68);

\node[text=laneBlue, anchor=west] at (0.18,3.73) {\LaneLabel{診斷線}};
\node[text=laneBlue, anchor=west] at (0.18,-3.85) {\LaneLabel{準則驗證線}};

\node[io, minimum width=2.30cm] (transcript) at (1.15,0.10)
{\ModuleTitle{Transcript}\\[-1pt]\ModuleSub{Input}};

\node[deterministic, minimum width=2.85cm] (retriever) at (4.50,2.90)
{\ModuleTitle{Similar-Case}\\[-1pt]\ModuleTitle{Retriever}\\[-1pt]\ModuleSub{Fixed retrieval}};

\node[outputbox, minimum width=1.95cm] (retrieved) at (8.26,2.90)
{\OutputTitle{Similar}\\[-1pt]\OutputTitle{Cases}};

\node[llm, minimum width=2.65cm] (diagnostician) at (11.93,2.90)
{\ModuleTitle{Diagnostician}\\[-1pt]\ModuleTitle{Agent}};

\node[outputbox, minimum width=3.15cm] (ranked) at (16.20,2.90)
{\OutputTitle{Ranked Top-3}\\[-1pt]\OutputSub{Proposed primary}\\[-1pt]\OutputSub{Optional comorbidity}};

\node[llm, minimum width=3.10cm] (checker) at (4.62,-2.70)
{\ModuleTitle{Criterion Checker}\\[-1pt]\ModuleTitle{Agent}};

\node[outputbox, minimum width=3.35cm, minimum height=1.48cm] (states) at (8.60,-2.70)
{\OutputTitle{Criterion states}\\[-1pt]\OutputSub{met / not met}\\[-1pt]\OutputSub{insufficient evidence}};

\node[deterministic, minimum width=2.85cm] (auditor) at (12.45,-2.70)
{\ModuleTitle{Compatibility}\\[-1pt]\ModuleTitle{Auditor}\\[-1pt]\ModuleSub{Rule aggregation}};

\node[outputbox, minimum width=3.15cm, minimum height=1.36cm] (compatible) at (16.20,-2.70)
{\OutputTitle{Criterion-compatible}\\[-1pt]\OutputTitle{set}\\[-1pt]\OutputSub{Compatibility results}};

\node[deterministic, minimum width=2.95cm] (finalization) at (16.20,0.10)
{\ModuleTitle{Finalization}\\[-1pt]\ModuleSub{DA / NtS}};

\node[finalout, minimum width=2.95cm] (finalprimary) at (19.90,0.10)
{\OutputTitle{Final primary}\\[-1pt]\OutputSub{diagnosis}};

\draw[mainarrow] (transcript.north) |- (retriever.west);
\draw[mainarrow] (transcript.east) -- (diagnostician.south);
\draw[mainarrow] (transcript.south) |- (checker.west);
\draw[mainarrow] (retriever.east) -- (retrieved.west);
\draw[mainarrow] (retrieved.east) -- (diagnostician.west);
\draw[mainarrow] (diagnostician.east) -- (ranked.west);
\draw[mainarrow] (checker.east) -- (states.west);
\draw[mainarrow] (states.east) -- (auditor.west);
\draw[mainarrow] (auditor.east) -- (compatible.west);
\node[inputlabel] (criteria) at (4.62,-4.62) {Configured criteria for all categories};
\draw[mainarrow] (criteria.north) -- (checker.south);
\draw[mainarrow] (ranked.south) -- (finalization.north);
\draw[mainarrow] (compatible.north) -- (finalization.south);
\draw[mainarrow] (finalization.east) -- (finalprimary.west);

\node[legendswatch, rounded corners=2pt, draw=iodraw, fill=iofill] at (2.70,-5.21) {};
\node[anchor=west, text=textgray] at (2.98,-5.21) {\LegendText{Input / final output}};
\node[legendswatch, rounded corners=2pt, draw=llmdraw, fill=llmfill] at (7.10,-5.21) {};
\node[anchor=west, text=textgray] at (7.38,-5.21) {\LegendText{LLM component}};
\node[legendswatch, draw=detdraw, fill=detfill, line width=1pt] at (10.60,-5.21) {};
\node[anchor=west, text=textgray] at (10.88,-5.21) {\LegendText{Deterministic component}};
\node[legendswatch, rounded corners=1pt, draw=outdraw, fill=outfill, dashed] at (15.55,-5.21) {};
\node[anchor=west, text=textgray] at (15.83,-5.21) {\LegendText{Recorded output}};

\end{tikzpicture}
\end{document}
"""
figure_src.parent.mkdir(parents=True, exist_ok=True)
figure_src.write_text(figure_text, encoding="utf-8")

# Final consistency checks before writing.
required = [
    r"\caption{Main datasets and their roles in the study.}",
    r"\caption{Primary-diagnosis selection methods.}",
    "Run the Diagnostician $K$ times, with $K=3$ or $5$, and use majority voting",
    "One advocate represents the diagnosis path and one represents the criterion path",
    r"\caption{Main internal comparison on the 1,000-case LingxiDiag held-out set.}",
    r"\caption{Primary-diagnosis selection results on the 925 MDD-5k cases.}",
    r"\includegraphics[width=1.0\textwidth]{fig_pipeline_round20c.pdf}",
]
for item in required:
    if item not in text:
        raise SystemExit(f"Required revised text is missing: {item}")

for item in forbidden_visible:
    if re.search(re.escape(item), text, flags=re.IGNORECASE):
        raise SystemExit(f"Forbidden legacy phrase remains: {item}")

# The main source should no longer use these engineering terms as visible words.
for word in [r"\bcontract\b", r"\blineage\b", r"\bposthoc\b"]:
    m = re.search(word, text, flags=re.IGNORECASE)
    if m:
        raise SystemExit(f"Engineering term remains: {m.group(0)} at offset {m.start()}")

thesis.write_text(text, encoding="utf-8")
print(f"Updated {thesis}")
print(f"Updated {figure_src}; workflow will build {figure_pdf}")
