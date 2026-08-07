from __future__ import annotations

from pathlib import Path

TIKZ_INSERT = r"""\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,fit,calc}
"""

CHAPTER_THREE = r"""\chapter{Study Architectures and Diagnostic Workflow}
\label{ch:architecture}

\section{Task Input and Diagnostic Scope}
\label{sec:input-diagnostic-scope}

The study processes one Chinese psychiatric interview transcript at a time. Each transcript is an ordered sequence of clinician and patient turns. The same preprocessed transcript is given to all compared methods. The methods cannot ask follow-up questions, so every output is based only on the information already present in the transcript.

The study focuses on fourteen configured ICD-10 diagnostic categories. These categories define the diagnoses that HiED may rank, check, and select. HiED does not cover the full ICD-10 diagnostic space. Subtype categories under F41 and F43 are later mapped to broader parent labels for evaluation, as described in Chapter~\ref{ch:data}.

For each configured category, HiED uses a study-specific set of diagnostic criteria informed by ICD-10 descriptions~\citep{who2019icd10}. These criteria are operational rules used in this study. They are not a verbatim copy of the ICD-10 manual and have not been independently validated as clinical diagnostic rules.

For each criterion, the Criterion Checker records one of three model-generated states: \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. A \texttt{met} state means that the transcript contains information that supports the criterion. A \texttt{not\_met} state means that the transcript contains information against the criterion. An \texttt{insufficient\_evidence} state means that the transcript does not provide enough information to make either judgment.

These states describe the evidence available in the fixed transcript under the study rules. They do not by themselves show that a diagnosis is clinically correct or that it should be selected as the primary diagnosis.

\begin{table}[htbp]
\centering
\caption{Configured ICD-10 diagnostic categories and their scoring parent labels.}
\label{tab:configured-profile-summary}
\small
\begin{tabularx}{\textwidth}{|p{3.0cm}|p{2.2cm}|X|}
\hline
ICD-10 code & Scoring parent & Diagnostic category\\
\hline
F20 & F20 & Schizophrenia\\
\hline
F31 & F31 & Bipolar affective disorder\\
\hline
F32 & F32 & Depressive episode\\
\hline
F39 & F39 & Unspecified mood disorder\\
\hline
F41.0 & F41 & Panic disorder\\
\hline
F41.1 & F41 & Generalized anxiety disorder\\
\hline
F41.2 & F41 & Mixed anxiety and depressive disorder\\
\hline
F42 & F42 & Obsessive-compulsive disorder\\
\hline
F43.1 & F43 & Post-traumatic stress disorder\\
\hline
F43.2 & F43 & Adjustment disorders\\
\hline
F45 & F45 & Somatoform disorders\\
\hline
F51 & F51 & Nonorganic sleep disorders\\
\hline
F98 & F98 & Other behavioral and emotional disorders\\
\hline
Z71 & Z71 & Counseling without a specific disorder\\
\hline
\end{tabularx}
\end{table}

\section{Compared Study Architectures}
\label{sec:compared-architectures}

This study compares two diagnostic architectures: a Single LLM baseline and HiED. Both architectures receive the same fixed psychiatric interview transcript and use the same configured diagnostic scope. Similar-case examples may also be provided under the retrieval conditions defined in Chapter~\ref{ch:experimental}.

The main difference between the two architectures is not whether the model can produce a diagnosis. Both architectures produce a committed primary diagnosis. The difference is which intermediate diagnostic outputs are recorded and available for evaluation.

\begin{figure}[htbp]
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    font=\sffamily\scriptsize,
    inputbox/.style={draw, rounded corners, fill=green!8, align=center, minimum height=0.75cm, text width=3.0cm},
    llmbox/.style={draw, rounded corners, fill=orange!15, align=center, minimum height=0.85cm, text width=3.0cm},
    detbox/.style={draw, double, rounded corners, fill=violet!10, align=center, minimum height=0.85cm, text width=3.0cm},
    artifactbox/.style={draw, dashed, rounded corners, fill=white, align=center, inner sep=4pt, text width=3.5cm},
    finalbox/.style={draw, very thick, rounded corners, fill=cyan!10, align=center, minimum height=0.85cm, text width=3.2cm},
    notebox/.style={draw, dotted, rounded corners, fill=yellow!7, align=center, inner sep=4pt, text width=4.2cm},
    panelbox/.style={draw, rounded corners, inner sep=7mm},
    flow/.style={-{Latex[length=2.2mm]}, thick},
    optionalflow/.style={-{Latex[length=2.2mm]}, thick, dashed}
]
\node[font=\sffamily\bfseries\normalsize] (stitle) at (0,7.4) {A. Single LLM baseline};
\node[inputbox] (sinput) at (-1.45,6.0) {Fixed transcript};
\node[inputbox, dashed] (scases) at (1.45,6.0) {Optional similar cases};
\node[llmbox] (sllm) at (0,4.45) {Single LLM};
\node[artifactbox, text width=4.0cm] (sout) at (0,2.35) {\textbf{Recorded final outputs}\\[2pt]Primary diagnosis\\Optional emitted labels};
\node[notebox] (snote) at (0,0.3) {No standardized ranked differential or diagnosis-specific criterion record under the evaluated output contract};
\coordinate (sbottom) at (0,-3.6);
\draw[flow] (sinput) -- (sllm);
\draw[optionalflow] (scases) -- (sllm);
\draw[flow] (sllm) -- (sout);
\node[panelbox, fit=(stitle)(sinput)(scases)(sllm)(sout)(snote)(sbottom)] (spanel) {};

\node[font=\sffamily\bfseries\normalsize] (htitle) at (9.1,7.4) {B. HiED two-path architecture};
\node[inputbox, text width=3.3cm] (hinput) at (9.1,6.15) {Fixed transcript};
\node[inputbox, dashed, text width=3.2cm] (hcases) at (5.7,6.15) {Optional similar cases};
\node[font=\bfseries] at (6.6,5.35) {Diagnosis path};
\node[llmbox] (hdiag) at (6.6,4.55) {Diagnostician};
\node[artifactbox, text width=4.1cm] (hdiagout) at (6.6,2.4) {\textbf{Recorded diagnosis outputs}\\[2pt]Ranked candidates (up to 5)\\Proposed primary\\Optional comorbid diagnosis};
\node[font=\bfseries] at (11.6,5.35) {Criterion-checking path};
\node[llmbox, text width=3.8cm] (hcheck) at (11.6,4.45) {Diagnosis-specific Criterion Checkers\\[-1pt]\scriptsize All 14 configured categories};
\node[artifactbox, text width=4.3cm] (hstates) at (11.6,2.35) {\textbf{Criterion states}\\[2pt]\texttt{met}\\\texttt{not\_met}\\\texttt{insufficient\_evidence}};
\node[detbox, text width=3.5cm] (hauditor) at (11.6,0.45) {Compatibility Auditor};
\node[artifactbox, text width=3.8cm] (hcompat) at (11.6,-1.05) {Criterion-compatible set};
\node[detbox, text width=3.7cm] (hfinal) at (8.9,-2.25) {Finalization policy\\[-1pt]\scriptsize DA or NtS};
\node[finalbox] (hcommitted) at (8.9,-3.55) {Committed primary diagnosis};
\draw[flow] (hinput) -- (hdiag);
\draw[flow] (hinput) -- (hcheck);
\draw[optionalflow] (hcases) -- (hdiag);
\draw[flow] (hdiag) -- (hdiagout);
\draw[flow] (hcheck) -- (hstates);
\draw[flow] (hstates) -- (hauditor);
\draw[flow] (hauditor) -- (hcompat);
\draw[flow] (hdiagout) -- (hfinal);
\draw[flow] (hcompat) -- (hfinal);
\draw[flow] (hfinal) -- (hcommitted);
\node[panelbox, fit=(htitle)(hinput)(hcases)(hdiag)(hdiagout)(hcheck)(hstates)(hauditor)(hcompat)(hfinal)(hcommitted)] (hpanel) {};
\end{tikzpicture}%
}
\caption{Comparison of the Single LLM and HiED study architectures. Both architectures receive the same fixed psychiatric interview transcript. Optional similar cases are provided to the direct diagnostic component only. The Single LLM records a primary diagnosis and optional emitted labels. HiED separately records a ranked differential diagnosis, a proposed primary diagnosis, diagnosis-specific criterion states, a criterion-compatible set, and the committed primary diagnosis. The figure compares observable study outputs and does not claim access to hidden model reasoning.}
\label{fig:single-vs-hied-architecture}
\label{fig:pipeline-thesis-rewrite}
\end{figure}
\FloatBarrier

\subsection{Single LLM Baseline}
\label{sec:single-architecture}

The Single LLM baseline reads the transcript and any optional similar-case examples in one diagnostic process. It directly returns a primary diagnosis and may also return additional diagnostic labels under its output format.

These additional labels are not produced under the same contract as HiED's ranked differential diagnosis. Therefore, the Single baseline does not provide a genuine ranked candidate list that can be used for the same candidate-coverage analysis as HiED. It also does not produce an independent criterion record for every configured diagnosis.

The absence of these recorded outputs does not mean that the model considered no alternative diagnoses. It means that the alternatives and their criterion states are not available as standardized outputs for separate analysis. The Single architecture is therefore evaluated mainly through its final primary and emitted diagnostic labels.

\subsection{HiED Two-Path Architecture}
\label{sec:hied-two-path-architecture}

HiED receives the same transcript but separates the study workflow into two connected paths. The diagnosis path produces a ranked list of candidate diagnoses, a proposed primary diagnosis, and an optional comorbid diagnosis. Similar-case examples, when used, are provided only to this path.

The criterion-checking path evaluates every configured diagnostic category using the same transcript. For each diagnosis, the Criterion Checker records whether each criterion is \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. A deterministic Compatibility Auditor then applies the study-specific rules and forms the criterion-compatible set.

A finalization step records one committed primary diagnosis using the available diagnostic and compatibility outputs. The Direct-Answer and Nominate-then-Select policies are described in Section~\ref{sec:primary-selection}.

The two paths are separate in their data flow and output roles. This does not mean that their errors are statistically independent. Both paths use the same transcript, and their model-based components may share similar model behavior.

\subsection{Recorded Output Differences}
\label{sec:recorded-output-differences}

Table~\ref{tab:single-hied-output-comparison} summarizes the recorded outputs available from the two architectures.

\begin{table}[htbp]
\centering
\caption{Recorded outputs available from the Single LLM and HiED study architectures.}
\label{tab:single-hied-output-comparison}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{4.4cm}|>{\centering\arraybackslash}p{3.2cm}|>{\centering\arraybackslash}X|}
\hline
\textbf{Recorded output} & \textbf{Single LLM} & \textbf{HiED}\\
\hline
Committed primary diagnosis & Yes & Yes\\
\hline
Optional secondary diagnostic labels & Available under the Single output format & Optional comorbid diagnosis from the diagnosis path\\
\hline
Genuine ranked differential diagnosis & No & Yes\\
\hline
Criterion state for each configured diagnosis & No & Yes\\
\hline
Criterion-compatible diagnosis set & No & Yes\\
\hline
Missing-information record at the criterion level & No & Yes, through \texttt{insufficient\_evidence} states\\
\hline
Separately observable diagnostic stages & Final emitted output only & Candidate generation, criterion checking, and primary selection\\
\hline
\end{tabularx}
\end{table}

These differences define the role of each architecture in this thesis. The Single LLM provides a direct diagnostic baseline. HiED provides a final diagnosis together with the ranked candidates and criterion-level records needed for stage-wise analysis and clinical review.

This comparison does not isolate the causal effect of using multiple agents. The two architectures differ in their workflow, number and role of model-based components, and output contracts. Their final performance should therefore be interpreted as a comparison between complete study architectures rather than as a controlled test of agent count alone.

\section{Diagnosis Path: Candidate Formation and Primary Proposal}
\label{sec:diagnosis-path}

The diagnosis path forms a differential diagnosis from the fixed psychiatric interview transcript. It may also receive similar labeled cases from the training source as examples. Its main outputs are a ranked candidate list, a proposed primary diagnosis, and an optional comorbid diagnosis.

\subsection{Optional Similar-Case Retrieval}
\label{sec:retrieval}

Similar-case retrieval provides labeled training cases as examples for the Diagnostician. These examples may show common ways of describing symptoms, possible diagnostic labels, and the expected output format. They are not evidence about the current patient and do not directly show which diagnosis is correct for the current transcript.

The study evaluates three retrieval conditions: no retrieval, global Top-5 retrieval, and parent-balanced retrieval. Global Top-5 retrieval selects the five most similar eligible cases. Parent-balanced retrieval limits repeated examples from the same scoring parent and increases the range of diagnostic categories shown to the Diagnostician. The complete comparison and selection procedure for these settings is described in Chapter~\ref{ch:experimental}.

Retrieved cases are provided only to the diagnosis path. The Criterion Checkers receive the current transcript and the criteria for their assigned diagnoses, but they do not receive the retrieved examples. Retrieval can therefore affect candidate formation and the proposed primary diagnosis, but it does not directly change the input to the criterion-checking path.

\subsection{Diagnostician Outputs}
\label{sec:diagnostician-outputs}

The Diagnostician receives the speaker-labeled transcript, the configured diagnostic scope, and any retrieved examples. It records three output roles:

\begin{enumerate}
    \item a ranked list of up to five candidate diagnoses;
    \item one proposed primary diagnosis selected from the three highest-ranked candidates; and
    \item at most one optional comorbid diagnosis.
\end{enumerate}

The ranked candidate list represents the model's differential diagnosis. It keeps possible alternatives visible even when they are not selected as primary. The main candidate-coverage analysis uses the first three distinct scoring-parent labels from this ranking, as defined in Chapter~\ref{ch:data}.

The proposed primary diagnosis is the Diagnostician's direct choice from the leading candidates. The ranking and the proposed primary are stored separately. A dataset reference diagnosis may therefore remain second or third in the ranking while another candidate is proposed as primary. This difference allows candidate coverage and primary selection to be evaluated separately.

The optional comorbid diagnosis has a different role from the ranked differential. A diagnosis that appears in the candidate list is not automatically treated as a comorbidity. The comorbid output indicates that the Diagnostician proposes that more than one disorder may be present at the same time.

The ranked list, proposed primary diagnosis, and optional comorbid diagnosis are outputs from the same Diagnostician. They should not be treated as independent model opinions. Their value in this study is that they record different diagnostic roles and allow later stages to be evaluated without inferring hidden model reasoning.

\section{Criterion-Checking Path: Criterion States and Compatibility}
\label{sec:criterion-checking-path}

The criterion-checking path examines the transcript at the diagnostic criterion level. Its purpose is to record which parts of each configured diagnosis are supported, not supported, or still unclear from the available transcript.

\subsection{Diagnosis-Specific Criterion Checkers}
\label{sec:criterion-checkers}

Each of the fourteen configured diagnostic categories has its own Criterion Checker. Every checker receives the same speaker-labeled transcript together with the study-specific criteria for one diagnostic category. The checkers do not receive the retrieved similar-case examples, and they do not use the Diagnostician's ranked candidate list.

All fourteen configured categories are checked for every case. The criterion-checking path is therefore not limited to the diagnoses that appear in the Diagnostician's Top-5. This design makes it possible for a diagnosis to appear in the criterion-compatible set even when it was not ranked among the leading candidates.

For each diagnostic criterion, the checker records one of three states. Table~\ref{tab:criterion-state-definitions} gives their definitions.

\begin{table}[htbp]
\centering
\caption{Criterion states recorded by the Criterion Checkers.}
\label{tab:criterion-state-definitions}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.6cm}|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Criterion state} & \textbf{Meaning in this study}\\
\hline
\texttt{met} & The transcript contains information that supports the criterion.\\
\hline
\texttt{not\_met} & The transcript contains information showing that the criterion is not met.\\
\hline
\texttt{insufficient\_evidence} & The transcript does not contain enough information to decide whether the criterion is met.\\
\hline
\end{tabularx}
\end{table}

An \texttt{insufficient\_evidence} state is not treated as negative evidence. It means that the current transcript does not provide enough information for either a \texttt{met} or a \texttt{not\_met} judgment.

The checker also records a short evidence note for each criterion when relevant information is identified. This note is kept for later review. It is a model-generated record and is not assumed to be a clinician-validated annotation or an exact quotation from the transcript.

\subsection{Compatibility Auditor}
\label{sec:compatibility-auditor}

After the Criterion Checkers finish, a deterministic Compatibility Auditor applies the study-specific rules for each configured diagnosis. Depending on the diagnosis, a rule may require particular core criteria, a minimum number of supported criteria, a required duration, or a combination of these conditions.

The auditor uses only the recorded criterion states. It does not reread the transcript, produce new clinical evidence, or change the checker outputs. The same set of criterion states therefore always produces the same compatibility result under the same rule.

For each diagnosis, the auditor records whether the diagnosis passes the configured compatibility rule. Diagnoses that pass are placed in the criterion-compatible set. The complete operational rules for the fourteen configured categories are reported in Appendix~\ref{app:configured-profile}.

\subsection{Interpretation of Criterion Compatibility}
\label{sec:criterion-compatibility-boundary}

A diagnosis in the criterion-compatible set has passed the study-specific rule using the criterion states recorded from the fixed transcript. This result has a limited meaning.

First, criterion compatibility does not show that the diagnosis is clinically correct. The criteria and aggregation rules are operationalizations used in this study, and the criterion states are model-generated.

Second, compatibility does not show that a diagnosis is the only possible diagnosis. Several disorders may pass their rules for the same transcript because psychiatric disorders can share symptoms and the transcript may not contain enough information to separate them.

Third, compatibility does not show that a diagnosis should be selected as primary. Criterion checking asks whether one diagnosis is supported under its own rule. Primary diagnosis selection requires comparison among several possible diagnoses.

The criterion-checking path therefore provides structured information for review. It shows which criteria are supported, which are not supported, and which still require more information. The final clinical meaning of these records must be judged by a clinician.

The criterion-checking path shows which diagnoses remain compatible with the available transcript, but it does not rank the compatible diagnoses against one another. The next section describes how HiED records the final primary diagnosis and how the evaluated finalization policies use the diagnosis and compatibility outputs.

\section{Primary Diagnosis Selection and Output Roles}
\label{sec:primary-selection}

The diagnosis and criterion-checking paths provide different views of the same transcript. The diagnosis path provides a ranked differential and a proposed primary diagnosis. The criterion-checking path provides criterion states and a criterion-compatible set. The primary-selection step records which diagnosis is finally committed as the system output.

\subsection{Diagnostic Output Roles}
\label{sec:diagnostic-output-roles}

HiED keeps several diagnostic output roles separate. Table~\ref{tab:diagnostic-output-roles} summarizes their meanings.

\begin{table}[htbp]
\centering
\caption{Diagnostic output roles recorded by HiED.}
\label{tab:diagnostic-output-roles}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.8cm}|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Output role} & \textbf{Meaning in this study}\\
\hline
Ranked candidate diagnosis & A possible diagnosis in the Diagnostician's ordered differential diagnosis. Its presence does not mean that the disorder is selected as primary or proposed as a comorbidity.\\
\hline
Proposed primary diagnosis & The diagnosis directly preferred by the Diagnostician before the finalization policy is applied.\\
\hline
Committed primary diagnosis & The single primary diagnosis recorded after the selected finalization policy is applied. This output is used for the main Top-1 evaluation.\\
\hline
Optional comorbid diagnosis & A second diagnosis proposed as being present at the same time as the primary diagnosis. It is different from a differential alternative.\\
\hline
Criterion-compatible diagnosis & A diagnosis that passes the study-specific compatibility rule. Its presence does not mean that it is clinically correct, comorbid, or the preferred primary diagnosis.\\
\hline
\end{tabularx}
\end{table}

These roles should not be combined without considering their meanings. A candidate diagnosis is an alternative under consideration. A comorbid diagnosis is proposed as an additional disorder that may be present. A criterion-compatible diagnosis has passed an operational rule. None of these roles alone determines which diagnosis should be committed as primary.

\subsection{Direct-Answer Policy}
\label{sec:direct-answer-policy}

Direct-Answer (DA) keeps the Diagnostician's proposed primary diagnosis as the committed primary diagnosis. The criterion states and criterion-compatible set remain available for review, but they do not replace the Diagnostician's choice.

DA may also retain one optional comorbid diagnosis. Its final output can therefore contain a primary diagnosis and an additional comorbid diagnosis. This output contract is important when interpreting multilabel measures such as Exact Match and F1.

DA represents the direct diagnostic decision of the diagnosis path. It is used as the main reference policy in the primary-selection experiments.

\subsection{Nominate-then-Select Policy}
\label{sec:nominate-then-select-policy}

Nominate-then-Select (NtS) uses both the ranked candidate list and the criterion-compatible set. It gives priority to a highly ranked candidate that also passes the configured compatibility rule. If the leading candidates do not pass, the policy uses the remaining compatibility information according to the predefined study rule.

NtS records one re-selected committed primary diagnosis. It does not retain the optional comorbid output used by DA. NtS therefore changes both the primary-selection rule and the number of diagnoses in the final output.

The complete fallback order, support-ratio definition, and tie-handling rules are reported in the experimental protocol and Appendix~\ref{app:supporting}. They are not part of the high-level architecture definition.

\subsection{Relationship Between DA and NtS}
\label{sec:da-nts-relationship}

DA and NtS reuse the same upstream HiED outputs. They receive the same Diagnostician ranking, proposed primary diagnosis, criterion states, and criterion-compatible set. Their difference is how these recorded outputs are used to commit one primary diagnosis.

This shared upstream information makes DA and NtS useful for studying the primary-selection stage. A difference between their committed primary diagnoses can be traced to the finalization policy rather than to a different transcript, a different candidate ranking, or a different criterion-checking result.

However, their comparison is not a pure comparison of primary selection for every evaluation measure. DA may retain an optional comorbid diagnosis, whereas NtS returns only one diagnosis. Their committed Top-1 results can be compared directly, but differences in Exact Match, Macro-F1, and Weighted-F1 may also reflect their different output sizes.

\subsection{Interpretation Boundary}
\label{sec:primary-selection-boundary}

The committed primary diagnosis is the system's final benchmark output. It is not an independently reviewed clinical primary diagnosis.

A disagreement between the committed primary and a dataset reference label may arise for several reasons. The system may select an inappropriate diagnosis, the transcript may not contain enough information to separate the leading candidates, or the dataset label may not represent a unique transcript-only clinical primary.

For this reason, this thesis refers to committed-primary agreement or benchmark disagreement rather than treating every mismatch as a confirmed clinical error.

The distinction among ranked candidates, proposed primary, criterion-compatible set, and committed primary is easier to see in a complete case. The next section follows one constructed psychiatric interview through the Single LLM and HiED architectures.

\section{Complete Worked Example}
\label{sec:worked-example}
\label{sec:running-example}

\subsection{Example Status and Purpose}

This section follows one complete constructed psychiatric interview through the Single LLM and HiED study architectures. The example extends the short interview excerpt used to explain criterion states and primary-selection policies.

The transcript is written for this thesis. It is not a patient record, a case copied from LingxiDiag, or an exported model trace. The outputs shown below are illustrative outputs that follow the study contracts. They are used only to explain the data flow and output roles and are not included in the quantitative evaluation.

The example contains evidence related to depressive and anxiety symptoms, together with questions about mania, psychotic symptoms, substance use, medical causes, and self-harm risk. It is complete for the purpose of demonstrating the study workflow, but it should not be treated as a complete real-world psychiatric assessment.

\subsection{Complete Constructed Transcript}

Table~\ref{tab:complete-worked-transcript} presents the complete speaker-labeled transcript used in this worked example.

\begingroup
\small
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.08}
\begin{longtable}{|>{\raggedright\arraybackslash}p{1.5cm}|>{\raggedright\arraybackslash}p{6.0cm}|>{\raggedright\arraybackslash}p{6.0cm}|}
\caption{Complete constructed psychiatric interview used in the worked example.}
\label{tab:complete-worked-transcript}
\label{tab:worked-example-transcript}\\
\hline
\textbf{Speaker} & \textbf{Original Chinese utterance} & \textbf{English translation}\\
\hline
\endfirsthead
\multicolumn{3}{c}{\tablename\ \thetable\ -- continued from the previous page}\\
\hline
\textbf{Speaker} & \textbf{Original Chinese utterance} & \textbf{English translation}\\
\hline
\endhead
Clinician & 最近最困擾你的事情是什麼？ & What has been troubling you most recently?\\
\hline
Patient & 這兩個星期幾乎每天心情都很低落，原本喜歡做的事情也都不想做。 & For the past two weeks, I have felt low almost every day and no longer want to do things that I previously enjoyed.\\
\hline
Clinician & 睡眠、食慾、精神和專注力有受到影響嗎？ & Have your sleep, appetite, energy, or concentration been affected?\\
\hline
Patient & 我常常很早就醒來，食慾也變差，整天沒有力氣，上班很難專心，做事情比以前慢很多。 & I often wake up very early, have less appetite, feel tired throughout the day, and have difficulty concentrating at work. I also work much more slowly than before.\\
\hline
Clinician & 最近會不會常覺得自己很沒用，或一直責怪自己？ & Have you often felt useless or blamed yourself recently?\\
\hline
Patient & 會，我覺得自己工作做不好，也沒有把家裡照顧好，常常覺得都是我的問題。 & Yes. I feel that I am doing poorly at work and not taking good care of my family. I often feel that everything is my fault.\\
\hline
Clinician & 你也提到會擔心。通常擔心哪些事情？持續多久了？ & You also mentioned feeling worried. What do you usually worry about, and how long has this continued?\\
\hline
Patient & 工作和家裡的事情都會擔心，腦子很難停下來，但我不確定是從什麼時候開始。好像心情變差後變得比較明顯。 & I worry about both work and family and find it difficult to stop thinking, but I am unsure when it began. It seems to have become more noticeable after my mood worsened.\\
\hline
Clinician & 擔心的時候，有沒有明顯坐立不安、肌肉緊繃、心悸或冒汗？ & When you feel worried, do you have clear restlessness, muscle tension, palpitations, or sweating?\\
\hline
Patient & 有時候肩膀很緊，心跳也會快一點，但不是每次都有，我自己也不太確定。 & Sometimes my shoulders feel tense and my heartbeat becomes faster, but this does not happen every time, and I am not very sure about it.\\
\hline
Clinician & 有沒有突然出現很強烈的害怕，幾分鐘內心跳很快、喘不過氣，覺得自己快要失控？ & Have you had sudden episodes of intense fear, with a rapid heartbeat, shortness of breath, or a feeling that you were losing control within a few minutes?\\
\hline
Patient & 沒有，沒有那種突然發作的情況。 & No. I have not had that kind of sudden episode.\\
\hline
Clinician & 以前有沒有一段時間特別亢奮、話很多、活動明顯增加，睡得很少也不覺得累？ & Have you ever had a period of unusually elevated mood, increased talking or activity, and very little sleep without feeling tired?\\
\hline
Patient & 沒有，我以前沒有這種情況。 & No. I have never experienced that.\\
\hline
Clinician & 最近有沒有聽到別人聽不到的聲音，或覺得有人要害你？ & Have you recently heard voices that other people could not hear, or felt that someone wanted to harm you?\\
\hline
Patient & 沒有。 & No.\\
\hline
Clinician & 最近有沒有大量喝酒、使用其他物質、開始新的藥物，或出現其他明顯的身體疾病？ & Have you recently used a large amount of alcohol, used other substances, started a new medication, or developed a clear medical problem?\\
\hline
Patient & 偶爾會喝一點酒，沒有用其他東西，也沒有開始新的藥。目前沒有知道的重大身體疾病。 & I occasionally drink a small amount of alcohol. I do not use other substances and have not started a new medication. I do not know of any major medical condition.\\
\hline
Clinician & 最近有沒有覺得活著沒有意義，或想過傷害自己？ & Have you recently felt that life was meaningless or thought about harming yourself?\\
\hline
Patient & 有時候會覺得很沒希望，但沒有想過傷害自己，也沒有計畫。 & I sometimes feel hopeless, but I have not thought about harming myself and have no plan.\\
\hline
Clinician & 以前有過類似的情況嗎？有沒有接受過精神科治療？ & Have you experienced a similar period before, or received psychiatric treatment?\\
\hline
Patient & 以前壓力大時會睡不好，但沒有像這次這麼嚴重，也沒有看過精神科。 & I have had poor sleep during stressful periods, but it was never this severe, and I have not received psychiatric treatment.\\
\hline
\end{longtable}
\endgroup

\subsection{Illustrative Single LLM Output}

Under the Single LLM output contract, an illustrative output for this transcript is shown in Table~\ref{tab:worked-example-single}.

\begin{table}[htbp]
\centering
\caption{Illustrative Single LLM output for the constructed transcript.}
\label{tab:worked-example-single}
\small
\begin{tabularx}{0.82\textwidth}{|>{\raggedright\arraybackslash}p{4.0cm}|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Output field} & \textbf{Illustrative output}\\
\hline
Primary diagnosis & F41.1 Generalized anxiety disorder\\
\hline
Optional additional diagnosis & F32 Depressive episode\\
\hline
Diagnosis-specific criterion states & Not produced\\
\hline
Standardized ranked differential & Not produced under this contract\\
\hline
\end{tabularx}
\end{table}

The additional F32 label is an emitted diagnostic label, not a standardized rank-two candidate under the HiED ranking contract. Therefore, the Single output should not be interpreted as the same ranked differential produced by HiED.

\subsection{Illustrative HiED Diagnosis-Path Output}

The diagnosis path keeps the candidate ranking and proposed primary diagnosis as separate outputs.

\begin{table}[htbp]
\centering
\caption{Illustrative diagnosis-path output for the constructed transcript.}
\label{tab:worked-example-diagnosis-path}
\small
\begin{tabularx}{0.86\textwidth}{|>{\raggedright\arraybackslash}p{4.1cm}|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Output role} & \textbf{Illustrative output}\\
\hline
Rank 1 & F41.1 Generalized anxiety disorder\\
\hline
Rank 2 & F32 Depressive episode\\
\hline
Rank 3 & F51 Nonorganic sleep disorder\\
\hline
Proposed primary diagnosis & F41.1 Generalized anxiety disorder\\
\hline
Optional comorbid diagnosis & None\\
\hline
\end{tabularx}
\end{table}

The ranking keeps F32 visible even though F41.1 is proposed as primary. This separation allows candidate availability and primary selection to be examined as different output views.

\subsection{Selected Criterion States}

Table~\ref{tab:worked-example-criteria} presents selected criterion states for three diagnoses. The states are illustrative applications of the study rules.

\begin{table}[htbp]
\centering
\caption{Selected illustrative criterion states for the constructed transcript.}
\label{tab:worked-example-criteria}
\footnotesize
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{2.5cm}|>{\raggedright\arraybackslash}p{4.0cm}|>{\centering\arraybackslash}p{2.6cm}|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Diagnosis} & \textbf{Criterion or evidence need} & \textbf{State} & \textbf{Information from the transcript}\\
\hline
F32 & Depressed mood and loss of interest & \texttt{met} & Both are reported almost every day.\\
\hline
F32 & Duration of at least two weeks & \texttt{met} & The patient reports a two-week period.\\
\hline
F32 & Associated symptoms and functional effect & \texttt{met} & Early waking, reduced appetite, low energy, poor concentration, self-blame, and reduced work function are reported.\\
\hline
F41.1 & Worry across more than one area & \texttt{met} & The patient reports worry about work and family.\\
\hline
F41.1 & Required duration & \texttt{insufficient\_evidence} & The patient cannot state when the worry began.\\
\hline
F41.1 & Associated anxiety symptoms & \texttt{insufficient\_evidence} & Some tension and increased heartbeat are reported, but their pattern and frequency remain unclear.\\
\hline
F31 & Previous manic episode & \texttt{not\_met} & The patient denies past elevated mood, increased activity, and reduced need for sleep.\\
\hline
\end{tabularx}
\end{table}

\subsection{Compatibility and Primary Selection}

Under the illustrative criterion states, F32 passes the configured compatibility rule. F41.1 does not enter the criterion-compatible set because the required duration remains unclear. F31 does not pass because no previous manic episode is supported.

Figure~\ref{fig:worked-example-flow} summarizes the same illustrative outputs and shows how DA and NtS use them differently.

\begin{figure}[htbp]
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    font=\sffamily\scriptsize,
    inputbox/.style={draw, rounded corners, fill=green!8, align=center, minimum height=0.85cm, text width=10.8cm},
    llmbox/.style={draw, rounded corners, fill=orange!15, align=center, minimum height=0.85cm, text width=3.7cm},
    detbox/.style={draw, double, rounded corners, fill=violet!10, align=center, minimum height=0.85cm, text width=3.7cm},
    artifactbox/.style={draw, dashed, rounded corners, fill=white, align=left, inner sep=5pt},
    policybox/.style={draw, rounded corners, fill=blue!7, align=center, inner sep=5pt, text width=4.3cm},
    finalbox/.style={draw, very thick, rounded corners, fill=cyan!10, align=center, inner sep=5pt, text width=4.2cm},
    missingbox/.style={draw, dotted, rounded corners, fill=yellow!10, align=center, inner sep=5pt, text width=8.8cm},
    flow/.style={-{Latex[length=2.2mm]}, thick},
    auditflow/.style={-{Latex[length=2.2mm]}, thick, dashed}
]
\node[inputbox] (exinput) at (6,11.0) {\textbf{Complete constructed transcript}\\[-1pt]\scriptsize Illustrative case---not a patient record or exported model trace};
\node[font=\bfseries] at (2.6,9.9) {Diagnosis path};
\node[llmbox] (exdiag) at (2.6,9.0) {Diagnostician};
\node[artifactbox, text width=4.5cm] (exdiagout) at (2.6,6.4) {\textbf{Illustrative ranked candidates}\\[2pt]1. F41.1 Generalized anxiety disorder\\2. F32 Depressive episode\\3. F51 Nonorganic sleep disorder\\[3pt]\textbf{Proposed primary:} F41.1\\\textbf{Optional comorbidity:} None};
\node[font=\bfseries] at (9.2,9.9) {Criterion-checking path};
\node[llmbox, text width=4.4cm] (excheck) at (9.2,9.0) {Diagnosis-specific Criterion Checkers\\[-1pt]\scriptsize All 14 categories checked; selected diagnoses shown};
\node[artifactbox, text width=7.0cm] (exstates) at (9.2,6.25) {\textbf{Selected criterion records}\\[2pt]\textbf{F32:} core symptoms \texttt{met}; duration \texttt{met}; associated symptoms and function \texttt{met} $\rightarrow$ included\\[3pt]\textbf{F41.1:} multi-area worry \texttt{met}; required duration \texttt{insufficient\_evidence}; associated symptoms \texttt{insufficient\_evidence} $\rightarrow$ not included\\[3pt]\textbf{F31:} previous manic episode \texttt{not\_met} $\rightarrow$ not included};
\node[detbox] (exauditor) at (9.2,3.65) {Compatibility Auditor\\[-1pt]\scriptsize Deterministic rule application};
\node[artifactbox, text width=3.8cm, align=center] (excompat) at (9.2,2.15) {\textbf{Criterion-compatible set}\\\texttt{\{F32\}}};
\node[font=\itshape] (exshared) at (6,1.1) {Same transcript and same recorded upstream outputs};
\node[policybox] (exda) at (3.1,-0.25) {\textbf{Direct-Answer}\\Keep the proposed primary};
\node[finalbox] (exdafinal) at (3.1,-1.65) {Committed primary\\\textbf{F41.1}};
\node[policybox] (exnts) at (8.9,-0.25) {\textbf{Nominate-then-Select}\\Select the highest-ranked criterion-compatible candidate};
\node[finalbox] (exntsfinal) at (8.9,-1.65) {Committed primary\\\textbf{F32}};
\node[missingbox] (exmissing) at (6,-3.35) {\textbf{Important missing information:} onset and duration of the anxiety symptoms};
\draw[flow] (exinput) -- (exdiag);
\draw[flow] (exinput) -- (excheck);
\draw[flow] (exdiag) -- (exdiagout);
\draw[flow] (excheck) -- (exstates);
\draw[flow] (exstates) -- (exauditor);
\draw[flow] (exauditor) -- (excompat);
\draw[flow] (exdiagout) -- (exda);
\draw[flow] (exdiagout) -- (exnts);
\draw[auditflow] (excompat) -- node[left, font=\tiny, align=center] {recorded\\for review} (exda);
\draw[flow] (excompat) -- (exnts);
\draw[flow] (exda) -- (exdafinal);
\draw[flow] (exnts) -- (exntsfinal);
\draw[flow] (exdafinal) -- (exmissing);
\draw[flow] (exntsfinal) -- (exmissing);
\end{tikzpicture}%
}
\caption{Illustrative HiED data flow for the complete constructed psychiatric interview. The diagnosis path ranks F41.1 above F32 and proposes F41.1 as primary. In the selected criterion records, F32 passes the configured compatibility rule, whereas the duration and associated symptoms required for F41.1 remain unclear. Direct-Answer keeps the proposed F41.1 primary diagnosis, while Nominate-then-Select commits F32 using the same upstream outputs. The example is constructed to explain the study architecture and does not represent a patient record, benchmark result, or clinically adjudicated diagnosis.}
\label{fig:worked-example-flow}
\end{figure}
\FloatBarrier

The selected diagnosis-level outputs are also summarized in Table~\ref{tab:worked-example-finalization}.

\begin{table}[htbp]
\centering
\caption{Illustrative compatibility and finalization outputs.}
\label{tab:worked-example-finalization}
\label{tab:running-example}
\small
\begin{tabularx}{0.9\textwidth}{|>{\raggedright\arraybackslash}p{4.2cm}|>{\raggedright\arraybackslash}X|}
\hline
\textbf{Output} & \textbf{Illustrative result}\\
\hline
Criterion-compatible set & \{F32\}\\
\hline
Diagnostician proposed primary & F41.1\\
\hline
DA committed primary & F41.1\\
\hline
NtS committed primary & F32\\
\hline
Remaining important uncertainty & The onset and duration of the anxiety symptoms remain unclear.\\
\hline
\end{tabularx}
\end{table}

DA keeps the Diagnostician's proposed primary diagnosis. NtS selects the highest-ranked diagnosis that also passes the compatibility rule. The two policies therefore produce different committed primary diagnoses while using the same transcript, ranking, and criterion states.

\subsection{What the Example Demonstrates}

This worked example demonstrates four features of the study architecture. First, a diagnosis may remain visible in the ranked differential even when it is not proposed as primary. Second, criterion checking may support one diagnosis while leaving another unresolved because important information is missing. Third, criterion compatibility and primary selection are different decisions. Fourth, DA and NtS may produce different committed diagnoses from the same upstream outputs.

The example does not establish that F32 is the clinically correct diagnosis or that NtS is a better policy. It contains no benchmark gold label and is not part of the quantitative evaluation. In the aggregate experiments, NtS does not consistently improve committed-primary agreement. The example is used only to make the architecture and output roles concrete.

\section{Chapter Summary}

This chapter described the two study architectures used in this thesis. The Single LLM baseline produces direct diagnostic outputs from one fixed transcript. HiED uses the same transcript but separately records a ranked differential diagnosis, diagnosis-specific criterion states, a criterion-compatible set, and a committed primary diagnosis.

HiED contains two connected paths. The diagnosis path forms and ranks possible diagnoses and proposes a primary diagnosis. The criterion-checking path records whether the available transcript supports, does not support, or provides insufficient information for each diagnostic criterion. A deterministic Compatibility Auditor then forms the criterion-compatible set under the study-specific rules.

The finalization policy uses the recorded outputs to commit one primary diagnosis. Direct-Answer keeps the Diagnostician's proposed primary diagnosis, whereas Nominate-then-Select uses the ranking and compatibility results to make a new selection. These policies share the same upstream outputs, but their final output contracts are not identical because Direct-Answer may also retain an optional comorbid diagnosis.

The complete worked example showed why these outputs must remain separate. A diagnosis may appear in the ranked differential without being selected as primary. A criterion may remain unclear because the transcript lacks important information. A diagnosis may also pass its own compatibility rule without being the preferred primary diagnosis.

These recorded outputs support the two main purposes of HiED. They allow candidate generation, criterion checking, and primary diagnosis selection to be analyzed separately, and they provide structured information that can be reviewed by clinicians. They do not reveal hidden model reasoning and should not be treated as clinician-validated diagnostic evidence.
"""


def main() -> None:
    candidates = [Path('school/main.tex'), Path('paper/school/HiED_school_version.tex')]
    target = next((p for p in candidates if p.exists()), None)
    if target is None:
        raise FileNotFoundError('Could not locate the School thesis source')

    text = target.read_text(encoding='utf-8')
    if '\\chapter{Study Architectures and Diagnostic Workflow}' in text:
        print(f'{target} already contains the Chapter 3 rewrite')
        return

    start_marker = '\\chapter{HiED System Architecture}'
    end_marker = '\\chapter{Datasets, Label Projection, and Evaluation Protocol}'
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise RuntimeError('Chapter markers were not found exactly once')

    start = text.index(start_marker)
    end = text.index(end_marker, start)
    old_block = text[start:end]
    if '\\ct{' in old_block or '\\wl{' in old_block:
        raise RuntimeError('Advisor comments were found inside Chapter 3; manual preservation is required')

    before_comment_counts = (text.count('\\ct{'), text.count('\\wl{'))

    package_anchor = '\\usepackage{amsmath,amssymb,graphicx}\n'
    if '\\usepackage{tikz}' not in text:
        if text.count(package_anchor) != 1:
            raise RuntimeError('Could not locate the graphics-package anchor')
        text = text.replace(package_anchor, package_anchor + TIKZ_INSERT, 1)

    updated = text[:start] + CHAPTER_THREE.strip() + '\n\n' + text[end:]

    after_comment_counts = (updated.count('\\ct{'), updated.count('\\wl{'))
    if before_comment_counts != after_comment_counts:
        raise RuntimeError('Advisor comment counts changed unexpectedly')

    required = [
        '\\chapter{Study Architectures and Diagnostic Workflow}',
        '\\label{fig:single-vs-hied-architecture}',
        '\\label{fig:pipeline-thesis-rewrite}',
        '\\label{fig:worked-example-flow}',
        '\\label{tab:configured-profile-summary}',
        '\\label{sec:retrieval}',
        '\\label{sec:primary-selection}',
        '\\label{sec:running-example}',
        'not a patient record, a case copied from LingxiDiag, or an exported model trace',
    ]
    for item in required:
        if item not in updated:
            raise RuntimeError(f'Missing required Chapter 3 content: {item}')

    forbidden_ch3 = [
        'Inference backend',
        'Structured JSON',
        'Checker recovery',
        'Vector search',
        '8,192-token context',
        'Qwen3-32B with 4-bit AWQ',
    ]
    new_start = updated.index('\\chapter{Study Architectures and Diagnostic Workflow}')
    new_end = updated.index(end_marker, new_start)
    new_block = updated[new_start:new_end]
    for item in forbidden_ch3:
        if item in new_block:
            raise RuntimeError(f'Implementation detail remains in Chapter 3: {item}')

    target.write_text(updated, encoding='utf-8')
    print(f'Updated {target}')
    print(f'Advisor comments preserved: CT={before_comment_counts[0]}, WL={before_comment_counts[1]}')


if __name__ == '__main__':
    main()
