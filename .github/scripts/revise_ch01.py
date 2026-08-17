from pathlib import Path

if Path("school/main.tex").exists():
    target = Path("school/main.tex")
elif Path("paper/school/HiED_school_version.tex").exists():
    target = Path("paper/school/HiED_school_version.tex")
else:
    raise SystemExit("Thesis source not found")

text = target.read_text(encoding="utf-8")
start_marker = r"\chapter{Introduction}"
end_marker = r"\chapter{Related Work}"

if text.count(start_marker) != 1 or text.count(end_marker) != 1:
    raise SystemExit("Chapter boundary markers are not unique")

start = text.index(start_marker)
end = text.index(end_marker, start)
old_block = text[start:end]

required_old = [
    r"\section{Background and Motivation}",
    r"\section{Problem Definition and Challenges}",
    r"\section{Overview of HiED and Study Scope}",
    r"\section{Contributions}",
    r"\section{Thesis Organization}",
    "same-case stage-wise output and evaluation contract",
    "The only clinician-facing study retained in this thesis",
]
for item in required_old:
    if item not in old_block:
        raise SystemExit(f"Expected Chapter 1 text not found: {item}")

new_block = r"""\chapter{Introduction}
\label{ch:introduction}

\section{Background and Motivation}

Taiwan's National Health Insurance system allows patients to access specialists and large medical centers directly. During a first psychiatric visit, the clinician must collect the patient's history, assess current symptoms and risks, and form an initial diagnosis from limited information. Important facts may still be missing, such as when the symptoms began, how long they have lasted, how they have changed, and whether another cause may explain them~\citep{lin2020outpatient}.

Patients may also describe emotional distress through everyday or physical complaints. In Chinese-speaking settings, they may first report poor sleep, fatigue, dizziness, chest tightness, or stomach problems instead of saying that they feel depressed or anxious~\citep{kleinman1982neurasthenia,ryder2008somatic}. The clinician must therefore turn a free-form conversation into clinical evidence while keeping the full context of the interview in view.

This task is difficult because several mental disorders share the same symptoms. Depression, anxiety, stress-related disorders, obsessive-compulsive disorder, somatic symptom disorders, and sleep disorders may all involve poor sleep, fatigue, poor concentration, and reduced daily function. A diagnosis cannot be made from one symptom alone. Each disorder has its own rules for key symptoms, symptom count, duration, effects on daily life, and the exclusion of other causes~\citep{who2019icd10}.

Even after these rules are checked, more than one diagnosis may still fit the same transcript. The symptoms may come from one main disorder, or more than one disorder may be present at the same time. The second case is called comorbidity~\citep{brown2001comorbidity}. In other cases, the transcript may not contain enough information to support one clear primary diagnosis. Structured diagnostic studies also report limited agreement for some common disorders~\citep{regier2013dsm5}.

A first psychiatric visit is therefore a comparison among possible diagnoses under incomplete evidence. It involves three linked decisions: forming candidate diagnoses, checking diagnostic criteria, and selecting a primary diagnosis while considering possible comorbidity. A mistake or uncertainty can appear at any of these stages. Time pressure may also increase the risk of focusing too early on one diagnosis~\citep{croskerry2003cognitive}.

For this reason, a useful decision-support system should provide more information than one final diagnosis. It should show the ranked candidate diagnoses, the state of each diagnostic criterion, and the information that is still missing. These outputs can help clinicians review the case and decide what should be checked next.

\section{Problem Definition and Challenges}
\label{sec:problem-definition}

Large language models can process clinical dialogue and produce diagnostic outputs. Medical multi-agent systems can also divide tasks across several model calls and combine their outputs~\citep{li2024taiwan,raballo2025,sarma2025,tang2024medagents,kim2024mdagents}. These methods are useful for psychiatric transcript analysis, but a final diagnosis alone does not show where a disagreement appears.

A benchmark disagreement can appear at different stages. A dataset reference diagnosis may never enter the candidate list. It may enter the list but fail the criterion check. It may also appear in both the candidate list and the criterion-compatible set, but another diagnosis may still be selected as primary. These cases require different improvements, but one final accuracy score groups them together.

In this thesis, a benchmark or dataset reference label is a diagnosis supplied by the dataset for scoring. It is not an independently reviewed clinical diagnosis. The recorded outputs therefore show where HiED agrees or disagrees with the benchmark; they do not by themselves show which diagnosis is clinically correct.

A strong same-source score may also reflect wording and label patterns that are specific to one dataset. It should not be treated as evidence of performance across different data sources. Same-source label prediction, cross-source transfer, and the amount of information provided for review are different questions.

The main technical problem studied in this thesis is how to make the three diagnostic decisions separately visible. This allows us to identify whether a benchmark disagreement appears during candidate generation, criterion checking, or primary diagnosis selection. Cross-source testing is used as an additional boundary analysis rather than as the main contribution of HiED.

\section{Overview of HiED and Study Scope}

This thesis proposes HiED, a hybrid, evidence-grounded multi-agent framework for Chinese psychiatric interview transcripts. HiED separates the diagnostic process into two paths. The diagnosis path produces a ranked differential diagnosis and a proposed primary diagnosis. The criterion-checking path records whether the transcript supports, does not support, or lacks enough information for each configured diagnostic criterion.

HiED keeps the ranked candidates, criterion states, criterion-compatible diagnoses, and final primary diagnosis as separate outputs. This allows candidate generation, criterion checking, and primary diagnosis selection to be evaluated separately. A direct Single LLM baseline reads the same transcript but mainly returns the final diagnostic output.

In this thesis, \emph{auditable} means that these outputs are saved and can be reviewed after the system finishes. It does not mean that the outputs are clinically correct. The completed experiments use synthetic Chinese dialogue datasets and contain no clinician-derived evaluation. A proposed single-psychiatrist review of selected LingxiDiag cases is described as future work. Real-patient evaluation is outside the scope of this thesis.

\section{Contributions}

This thesis makes two main contributions.

First, it proposes a two-path hybrid framework for psychiatric differential diagnosis. The diagnosis path produces ranked candidate diagnoses, while the criterion-checking path records criterion-level support and forms a criterion-compatible set. HiED keeps these outputs together with the final primary diagnosis so that they can be reviewed separately.

Second, it introduces a stage-wise evaluation method for locating benchmark disagreement. The method separately measures whether a reference diagnosis appears in the Top-3, enters the criterion-compatible set, and is selected as the final primary diagnosis. This analysis is applied to two synthetic Chinese dialogue datasets. The results describe benchmark agreement under the tested settings and do not establish the clinically correct diagnosis.

\section{Thesis Organization}

Chapter~\ref{ch:related} reviews related work on psychiatric large language models, medical multi-agent systems, criterion-based diagnosis, and auditable decision support. Chapter~\ref{ch:architecture} compares the Single LLM and HiED study architectures and follows a complete transcript through the recorded outputs. Chapter~\ref{ch:data} defines the datasets, label mapping, output views, evaluation measures, and statistical methods. Chapter~\ref{ch:experimental} describes the experimental design and the proposed future psychiatrist review. Chapters~\ref{ch:results} and~\ref{ch:external} report the internal and external synthetic results. Chapter~\ref{ch:error} examines the main recorded disagreement patterns. Chapters~\ref{ch:discussion}--\ref{ch:conclusion} discuss the findings, limitations, conclusions, and future work.

"""

updated = text[:start] + new_block + text[end:]

checks = [
    r"\section{Background and Motivation}",
    r"\section{Problem Definition and Challenges}",
    r"\section{Overview of HiED and Study Scope}",
    r"\section{Contributions}",
    r"\section{Thesis Organization}",
    "A proposed single-psychiatrist review of selected LingxiDiag cases is described as future work.",
    "it proposes a two-path hybrid framework",
    "it introduces a stage-wise evaluation method",
]
chapter = updated[updated.index(start_marker):updated.index(end_marker, updated.index(start_marker))]
for item in checks:
    if chapter.count(item) != 1:
        raise SystemExit(f"Chapter 1 validation failed for: {item}")

for forbidden in [
    "same-case stage-wise output and evaluation contract",
    "The only clinician-facing study retained in this thesis",
    "Compatibility Auditor then forms",
]:
    if forbidden in chapter:
        raise SystemExit(f"Legacy Chapter 1 wording remains: {forbidden}")

if updated[:start] != text[:start] or updated[updated.index(end_marker):] != text[end:]:
    raise SystemExit("Text outside Chapter 1 changed")

target.write_text(updated, encoding="utf-8")
print(f"Updated only Chapter 1 in {target}")
