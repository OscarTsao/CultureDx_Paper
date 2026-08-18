from pathlib import Path


if Path("school/main.tex").exists():
    thesis_path = Path("school/main.tex")
    figure_source_path = Path("figures/src/fig_pipeline_round20c_tikz.tex")
elif Path("paper/school/HiED_school_version.tex").exists():
    thesis_path = Path("paper/school/HiED_school_version.tex")
    figure_source_path = Path("paper/figures/src/fig_pipeline_round20c_tikz.tex")
else:
    raise SystemExit("Could not locate the formal thesis source.")


def replace_range(text: str, start: str, end: str, replacement: str, name: str) -> str:
    start_index = text.find(start)
    if start_index < 0:
        raise RuntimeError(f"Missing start marker for {name}: {start}")
    end_index = text.find(end, start_index + len(start))
    if end_index < 0:
        raise RuntimeError(f"Missing end marker for {name}: {end}")
    return text[:start_index] + replacement.rstrip() + "\n\n" + text[end_index:]


def replace_once(text: str, old: str, new: str, name: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match for {name}, found {count}.")
    return text.replace(old, new, 1)


text = thesis_path.read_text(encoding="utf-8")

# 1. Refocus Section 1.2 on the actual technical problem and challenges.
problem_section = r"""\section{Problem Definition and Challenges}
\label{sec:problem-definition}

Large language models can process clinical dialogue, and medical
multi-agent systems can divide diagnostic tasks across several model
calls~\citep{li2024taiwan,raballo2025,sarma2025,tang2024medagents,kim2024mdagents}.
However, a final diagnosis alone does not show how the system reached
that result or where a benchmark disagreement became visible.

The first challenge is incomplete evidence. This thesis studies
differential diagnosis from one fixed psychiatric interview transcript.
The system cannot ask follow-up questions or use information that is
absent from the transcript. Important distinctions, such as symptom
onset, duration, episode history, symptom order, and exclusionary causes,
may therefore remain unresolved.

The second challenge is comparison among compatible diagnoses. Several
disorders may pass their own rules for the same transcript. The system
must still decide which diagnosis best explains the current presentation,
which diagnoses should remain differential alternatives, and whether
another diagnosis should be recorded as comorbid.

The third challenge is evaluation. A final accuracy score does not show
whether a reference diagnosis was omitted from the candidate list, did
not enter the criterion-compatible set, or remained available but was
not selected as the final primary diagnosis. These patterns require
different improvements.

The main problem addressed in this thesis is therefore how to keep
candidate formation, criterion checking, and primary-diagnosis selection
separately visible for the same case. The resulting analysis describes
agreement with dataset reference labels and does not determine the
clinically correct diagnosis.
"""
text = replace_range(
    text,
    r"\section{Problem Definition and Challenges}",
    r"\section{Overview of HiED and Study Scope}",
    problem_section,
    "Section 1.2",
)

text = replace_once(
    text,
    r"Chapter~\ref{ch:experimental} describes the experimental design and the proposed future psychiatrist review.",
    r"Chapter~\ref{ch:experimental} describes the experimental design for the completed computational studies.",
    "Chapter 1 organization sentence",
)

# 2 and 3. Expand the Chapter 3 worked example to show the full two-path flow.
worked_example = r"""\section{Worked Example of the Two-Path Workflow}
\label{sec:running-example}
\label{sec:worked-example}

This constructed example follows one transcript through the diagnosis
path, the criterion-checking path, and the final selection step. It is
not a patient record, a LingxiDiag case, or a quantitative result.

Table~\ref{tab:worked-example-flow} summarizes the outputs produced at
each stage.

\begin{table}[htbp]
\centering
\caption{Illustrative outputs from the two-path workflow.}
\label{tab:worked-example-flow}
\small
\renewcommand{\arraystretch}{1.10}
\begin{tabularx}{\textwidth}
{|>{\raggedright\arraybackslash}p{3.35cm}|
 >{\raggedright\arraybackslash}X|}
\hline
\textbf{Stage} & \textbf{Illustrative output}\\
\hline
Transcript evidence &
Low mood and loss of interest have continued for two weeks. Sleep,
energy, concentration, and work function are affected. Worry is present,
but its onset and related physical symptoms are unclear. The patient
denies earlier periods of elevated mood and reduced need for sleep.\\
\hline
Similar-case retrieval &
Similar training cases are supplied only to the Diagnostician. They guide
candidate formation but are not treated as evidence about the current
patient.\\
\hline
Diagnostician &
Ranked Top-3: F41.1, F32, F51. Proposed primary: F41.1. No optional
comorbid diagnosis is emitted.\\
\hline
F32 Criterion Checker &
Core symptoms, associated symptoms, two-week duration, and functional
impairment are marked \texttt{met}.\\
\hline
F41.1 Criterion Checker &
Worry is supported, but the required duration and associated symptoms
are marked \texttt{insufficient evidence}.\\
\hline
F51 Criterion Checker &
Sleep disturbance is present, but the configured frequency and duration
requirements are marked \texttt{insufficient evidence}.\\
\hline
F31 Criterion Checker &
A previous manic episode is marked \texttt{not met}.\\
\hline
Compatibility Auditor &
The category-level set is
$L_{\mathrm{cat}}=\{\mathrm{F32}\}$. After projection, the parent-level
set is $L_{\mathrm{par}}=\{\mathrm{F32}\}$.\\
\hline
\end{tabularx}
\renewcommand{\arraystretch}{1.0}
\end{table}

The two finalization policies use the same transcript, ranked candidates,
criterion states, and compatible set. Table~\ref{tab:worked-example-finalization}
shows how their selection rules produce different final outputs.

\begin{table}[htbp]
\centering
\caption{Finalization of the illustrative example.}
\label{tab:running-example}
\label{tab:worked-example-finalization}
\small
\renewcommand{\arraystretch}{1.10}
\begin{tabularx}{0.92\textwidth}
{|>{\raggedright\arraybackslash}p{2.4cm}|
 >{\raggedright\arraybackslash}X|
 >{\centering\arraybackslash}p{2.7cm}|}
\hline
\textbf{Policy} & \textbf{Selection rule} & \textbf{Final primary}\\
\hline
Direct-Answer &
Keep the primary diagnosis proposed by the Diagnostician. &
F41.1\\
\hline
Nominate-then-Select &
Select the highest-ranked Top-3 category that also belongs to
$L_{\mathrm{cat}}$. &
F32\\
\hline
\end{tabularx}
\renewcommand{\arraystretch}{1.0}
\end{table}

The example shows the role of every recorded output. Retrieval supports
candidate formation, the Criterion Checkers produce diagnosis-specific
states, the Compatibility Auditor forms the compatible set, and the
finalization policy determines which available diagnosis becomes the
final primary diagnosis.

The example does not show that F32 is the clinically correct diagnosis
or that NtS is the better method. It shows only how the same upstream
outputs can lead to different final diagnoses when the selection rule
changes.
"""
text = replace_range(
    text,
    r"\section{Illustrative Example}",
    r"\section{Chapter Summary}",
    worked_example,
    "Chapter 3 worked example",
)

# 4. Move the metric audit from Chapter 4 to Appendix B.
audit_start = r"\subsection{Case-Level Metric Audit and Recalculation Boundary}"
audit_end = r"\section{Case-Level Indicators for Disagreement Localization}"
start_index = text.find(audit_start)
end_index = text.find(audit_end, start_index)
if start_index < 0 or end_index < 0:
    raise RuntimeError("Could not locate the Chapter 4 metric-audit subsection.")
audit_block = text[start_index:end_index]
audit_block = audit_block.replace(
    audit_start,
    r"\section{Metric Recalculation and Result Provenance}",
    1,
)
main_audit_note = r"""The preserved HiED case-level outputs were independently rescored and
reproduced the reported metrics. Detailed recalculation results,
output-cardinality statistics, and result-provenance boundaries are
reported in Appendix~\ref{app:supporting}.

"""
text = text[:start_index] + main_audit_note + text[end_index:]
appendix_marker = r"\section{Main-System Configuration}"
appendix_index = text.find(appendix_marker)
if appendix_index < 0:
    raise RuntimeError("Could not locate the Appendix B main-system section.")
text = text[:appendix_index] + audit_block.rstrip() + "\n\n" + text[appendix_index:]

# 5 and 6. Remove the repeated Chapter 5 population table and move the
# psychiatrist-review protocol fully to Chapter 11 Future Work.
chapter5_intro = r"""\chapter{Experimental Design}
\label{ch:experimental}

This chapter explains how the completed computational experiments address
RQ1--RQ5. Chapter~\ref{ch:data} defines the datasets, data splits,
evaluation populations, label mapping, and measures. The validation set
is used only for configuration selection, the fixed LingxiDiag held-out
set is used for internal evaluation, and MDD-5k is used for external
synthetic evaluation.

All completed experiments use synthetic Chinese psychiatric dialogues,
and no clinician-derived evaluation was conducted. The proposed
psychiatrist review is described as future work in
Chapter~\ref{ch:conclusion}.
"""
text = replace_range(
    text,
    r"\chapter{Experimental Design}",
    r"\section{Retrieval Selection and Internal Comparison}",
    chapter5_intro,
    "Chapter 5 opening and repeated population section",
)

text = replace_range(
    text,
    r"\section{Proposed Psychiatrist Review}",
    r"\chapter{Internal Evaluation Results}",
    "",
    "Chapter 5 proposed psychiatrist review",
)

future_review_heading = (
    r"\paragraph{Conduct a single-psychiatrist review of benchmark-label"
    "\n"
    r"alignment.}"
)
future_review_with_labels = (
    future_review_heading
    + "\n"
    + r"\label{sec:clinical-evaluation-plan}"
    + "\n"
    + r"\label{sec:lingxidiag-pilot-review}"
)
text = replace_once(
    text,
    future_review_heading,
    future_review_with_labels,
    "Chapter 11 future-review labels",
)

# 7. Make Table 7.4 use real flexible columns so its right border stays
# inside the text block.
old_table_spec = r"""\small
\begin{tabularx}{\textwidth}
{|>{\raggedright\arraybackslash}p{3.3cm}|
 >{\raggedright\arraybackslash}p{3.3cm}|
 c|c|c|}"""
new_table_spec = r"""\small
\begingroup
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabularx}{\textwidth}
{|>{\raggedright\arraybackslash}X|
 >{\raggedright\arraybackslash}X|
 >{\centering\arraybackslash}p{1.45cm}|
 >{\centering\arraybackslash}p{1.45cm}|
 >{\centering\arraybackslash}p{1.45cm}|}"""
text = replace_once(text, old_table_spec, new_table_spec, "Table 7.4 column layout")

lexical_label_index = text.find(r"\label{tab:lexical-transfer-rewrite}")
if lexical_label_index < 0:
    raise RuntimeError("Could not locate Table 7.4.")
lexical_table_end = text.find(r"\end{table}", lexical_label_index)
if lexical_table_end < 0:
    raise RuntimeError("Could not locate the end of Table 7.4.")
lexical_block_start = text.rfind(r"\begin{table}", 0, lexical_label_index)
lexical_block = text[lexical_block_start:lexical_table_end]
if r"\end{tabularx}

\parbox" not in lexical_block:
    raise RuntimeError("Unexpected Table 7.4 structure.")
lexical_block_new = lexical_block.replace(
    r"\end{tabularx}

\parbox",
    r"\end{tabularx}
\endgroup

\parbox",
    1,
)
text = text[:lexical_block_start] + lexical_block_new + text[lexical_table_end:]

# Final structural checks.
required = [
    r"\section{Worked Example of the Two-Path Workflow}",
    r"\section{Metric Recalculation and Result Provenance}",
    r"\label{sec:clinical-evaluation-plan}",
    r"\label{tab:lexical-transfer-rewrite}",
]
for marker in required:
    if marker not in text:
        raise RuntimeError(f"Missing required final marker: {marker}")

for removed in [
    r"\section{Study Sequence and Analysis Populations}",
    r"\label{tab:analysis-populations}",
    r"\section{Proposed Psychiatrist Review}",
    r"\subsection{Case-Level Metric Audit and Recalculation Boundary}",
]:
    if removed in text:
        raise RuntimeError(f"Removed marker still present: {removed}")

thesis_path.write_text(text, encoding="utf-8")

figure_text = figure_source_path.read_text(encoding="utf-8")
figure_text = replace_once(
    figure_text,
    r"\draw[mainarrow] (transcript.east) -- (diagnostician.south);",
    r"\draw[mainarrow] (transcript.east) -| (diagnostician.south);",
    "Figure 3.1 transcript-to-Diagnostician arrow",
)
figure_source_path.write_text(figure_text, encoding="utf-8")

print(f"Patched {thesis_path}")
print(f"Patched {figure_source_path}")
