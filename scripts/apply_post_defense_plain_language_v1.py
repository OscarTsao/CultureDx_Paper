from __future__ import annotations

from pathlib import Path


ZH_ABSTRACT = r"""精神科初診逐字稿中的鑑別診斷，是在資訊不完整時比較多個可能診斷的過程。多個疾病可能同時符合一份逐字稿中的症狀，但醫師通常仍要選出一個主診斷。用來區分疾病的重要資訊，例如症狀持續時間、發病先後、其他可能病因與共病關係，不一定會在一次初診中被完整問出。大型語言模型可以閱讀這類逐字稿，但文字表達流暢不代表模型一定能可靠地完成鑑別診斷。

現有研究多以最後的診斷準確率評估系統。然而，答錯可能發生在不同階段：系統可能沒有把資料集標準答案列入候選，也可能沒有找到足夠的準則證據，或是已經找到該診斷並通過準則檢查，最後卻選了另一個主診斷。單一準確率無法說明問題發生在哪一個階段，也無法告訴研究者應該改善候選形成、準則核對，還是最後的選擇。

本研究提出 HiED，一套用於中文精神科初診逐字稿的混合式證據多代理決策支援框架。HiED 將流程分成候選形成、準則核對與主診斷選擇三個階段。系統會輸出排序後的候選診斷，並把每項診斷準則標記為符合、不符合或資訊不足。系統也會保留相容診斷集合與最後的主診斷，讓每一個階段都能被檢查與分析。

分階段分析顯示，主診斷選擇是本研究兩個合成資料集中的最大已記錄瓶頸。在內部 915 個可進行準則分析的案例中，有 272 例（29.7\%）的資料集標準答案已進入前三個候選，也通過準則檢查，但最後沒有被選為主診斷；外部資料中也有 225／878 例（25.6\%）出現相同情況。本研究的技術貢獻，是提出一個能分別記錄與評估三個診斷階段的架構。其決策支援價值，則是提供候選診斷與逐項準則狀態，讓醫師可以先篩選可能疾病、查看支持或排除資訊，並找出仍需補充的內容。HiED 的目的不是取代醫師，而是提供更多可檢查的資訊來支援判斷。題目所稱的臺灣情境，指系統預期使用的語言與臨床場域，並不代表已完成臺灣真實病人的臨床驗證。目前結果來自合成中文逐字稿，系統是否能改善真實臨床工作仍需透過醫師與真實病人資料進一步驗證。"""


EN_ABSTRACT = r"""Differential diagnosis from a first psychiatric interview means comparing several possible disorders with incomplete information. More than one disorder may fit the same transcript, but one is usually chosen as the primary diagnosis. Important details, such as symptom duration, the order in which symptoms began, other possible causes, and comorbidity, may be missing from one visit. Large language models can read these transcripts, but fluent language does not ensure a reliable differential diagnosis.

Most studies report only the final diagnosis score. A wrong final answer can come from different stages. The benchmark gold diagnosis may be missing from the candidate list, may not pass the criterion check, or may be present in both outputs but still not be chosen as the primary diagnosis. One accuracy score cannot show which stage caused the disagreement or which part of the system should be improved.

We propose HiED, a hybrid, evidence-grounded multi-agent decision-support framework for Chinese psychiatric interview transcripts. HiED separates the task into candidate generation, criterion checking, and primary diagnosis selection. It returns a ranked list of possible diagnoses and marks each diagnostic criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. The system also keeps the criterion-compatible set and final diagnosis so that each stage can be reviewed and studied.

The stage-wise analysis shows that primary diagnosis selection is the largest recorded bottleneck in the two tested synthetic datasets. Among 915 internal cases available for criterion analysis, 272 (29.7\%) contained a benchmark gold diagnosis in both the Top-3 and the criterion-compatible set, but another diagnosis was chosen as primary. The same pattern appeared in 225 of 878 external cases (25.6\%). The technical contribution of this work is a framework that records and evaluates these stages separately. Its decision-support value is the structured candidate and criterion information that clinicians can review when screening possible diagnoses and deciding what information is still needed. HiED is designed to support clinicians, not replace them. The Taiwanese context in the title refers to the intended language and clinical setting; it does not mean that the system has been validated with Taiwanese patients. The current results come from synthetic Chinese transcripts, and the effect on clinical work still requires evaluation with clinicians and real-patient data."""


CHAPTER_ONE = r"""\section{Background and Motivation}

Psychiatric outpatient care in Taiwan is easy to access, but large hospitals also face a heavy workload. Under National Health Insurance, patients may visit different levels of care without a referral, and a large medical center may handle more than ten thousand outpatient visits across departments in one day~\citep{lin2020outpatient}. During a first psychiatric visit, the clinician must take the patient's history, observe the mental state, screen for risk, and form an initial diagnosis within limited time. The note or transcript may still miss important facts about onset, duration, illness course, medical or substance-related causes, and past treatment.

Patients may also describe distress in indirect ways. In Chinese-speaking settings, they may first talk about insomnia, fatigue, dizziness, chest tightness, or stomach problems instead of naming low mood or anxiety directly~\citep{kleinman1982neurasthenia,ryder2008somatic}. Taiwanese visits may also mix Mandarin, Taiwanese expressions, and local clinical terms. The same condition can therefore be described in many ways.

Common psychiatric disorders also share many symptoms. Depression, anxiety, stress-related disorders, obsessive-compulsive disorder, somatic symptom disorders, and sleep disorders can all involve poor sleep, fatigue, low concentration, and problems in daily life. Diagnosis depends on more than one symptom. Different disorders require different core symptoms, symptom counts, duration, effects on daily function, and exclusion rules~\citep{who2019icd10}. Even after these criteria are checked, several disorders may still fit the same transcript. Symptoms of depression and anxiety, for example, may reflect comorbidity or overlap within one main condition~\citep{brown2001comorbidity}. Agreement is also limited for some common disorders, even in structured diagnostic studies~\citep{regier2013dsm5}.

A first psychiatric visit is therefore not a simple one-label classification task. The clinician must compare several possible disorders with incomplete evidence, choose a working primary diagnosis, keep other likely diagnoses in view, and note what information is still missing. Time pressure can increase the risk of early anchoring or premature closure when several disorders share similar symptoms~\citep{croskerry2003cognitive}.

\section{Problem Definition and Challenges}
\label{sec:problem-definition}

Large language models can read free-form dialogue, organize symptom information, retrieve examples, and produce structured outputs. Multi-agent systems can divide the task among different roles and combine their outputs~\citep{li2024taiwan,raballo2025,sarma2025,tang2024medagents,kim2024mdagents}. These tools are useful, but they do not by themselves make differential diagnosis reliable.

A final disagreement can start at different stages. The benchmark gold diagnosis may never enter the candidate list. It may enter the list but fail the criterion check. It may also appear in both the candidate list and the criterion-compatible set but still not be chosen as the primary diagnosis. These cases need different fixes, but one final accuracy score groups them together.

A second issue is corpus dependence. A text classifier may learn words and label patterns that are common in one corpus. It can perform well when its training and test cases come from the same source, but its performance may fall when the wording, class balance, or data-generation process changes. Same-corpus label accuracy, cross-corpus transfer, and the amount of review information provided by a system are therefore different questions.

This thesis studies both problems. It asks where disagreement is recorded in the diagnostic process and what structured information can be kept for review. The next section introduces HiED, which makes candidate generation, criterion checking, and primary diagnosis selection separately visible.

\section{Overview of HiED and Study Scope}

HiED is a hybrid multi-agent decision-support framework for Chinese transcripts of first psychiatric visits. It is motivated by the Taiwanese outpatient setting, but the completed quantitative tests use synthetic Chinese dialogue datasets. The LingxiDiag psychiatrist pilot and CGMH real-world study are ongoing and are not part of the current quantitative results.

HiED uses two paths. In the first path, an LLM-based Diagnostician ranks possible diagnoses and gives a primary diagnosis. In the second path, diagnosis-specific Criterion Checkers examine the same transcript using study-specific criteria based on ICD-10. Each checker marks a criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. A deterministic Compatibility Auditor then forms the criterion-compatible set. A finalization policy records the committed primary diagnosis.

The system keeps the ranked candidate list, criterion states, supporting text, compatibility results, and committed diagnosis as separate outputs. These records support two uses. First, they allow stage-wise analysis of where a benchmark disagreement appears. Second, they provide a clinician with possible diagnoses, the evidence state of each criterion, and the information that is still missing. HiED is designed to support review, not to replace the clinician. This thesis does not yet measure whether the system saves time or improves clinical outcomes.

\section{Contributions}

This thesis makes two main contributions.

First, it presents a stage-wise technical framework for psychiatric decision support. HiED separates candidate generation, criterion checking, and primary diagnosis selection, and it records the output of each stage. This design shows whether a benchmark disagreement comes from a missing candidate, a criterion-checking difference, or the final primary choice. Using this framework, the study finds that primary diagnosis selection is the largest recorded bottleneck in the tested synthetic datasets.

Second, it provides structured information for clinical review instead of only one final label. HiED returns a ranked candidate list and marks each diagnostic criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. It also keeps the criterion-compatible set and final selection trace. These outputs are designed to help clinicians screen possible diagnoses, review supporting or conflicting evidence, and identify what information still needs to be collected. Their effect on clinical speed, accuracy, and safety still requires direct clinical evaluation."""


def replace_body(text: str, start_marker: str, end_marker: str, body: str) -> str:
    if text.count(start_marker) != 1:
        raise RuntimeError(f"Expected one start marker: {start_marker!r}")
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + body.strip() + "\n\n" + text[end:]


def replace_block(text: str, start_marker: str, end_marker: str, block: str) -> str:
    if text.count(start_marker) != 1:
        raise RuntimeError(f"Expected one block start: {start_marker!r}")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + block.strip() + "\n\n" + text[end:]


def main() -> None:
    candidates = [
        Path("school/main.tex"),
        Path("paper/school/HiED_school_version.tex"),
    ]
    target = next((path for path in candidates if path.exists()), None)
    if target is None:
        raise FileNotFoundError("Could not find the School thesis source file")

    original = target.read_text(encoding="utf-8")
    comment_counts = (original.count("\\ct{"), original.count("\\wl{"))

    updated = replace_body(
        original,
        "\\addcontentsline{toc}{chapter}{中文摘要}\n",
        "\\noindent\\textbf{關鍵詞：}",
        ZH_ABSTRACT,
    )
    updated = replace_body(
        updated,
        "\\addcontentsline{toc}{chapter}{Abstract}\n",
        "\\noindent\\textbf{Keywords:}",
        EN_ABSTRACT,
    )
    updated = replace_block(
        updated,
        "\\section{Background and Motivation}",
        "\\section{Thesis Organization}",
        CHAPTER_ONE,
    )

    if (updated.count("\\ct{"), updated.count("\\wl{")) != comment_counts:
        raise RuntimeError("Advisor comment counts changed unexpectedly")

    target.write_text(updated, encoding="utf-8")
    print(f"Updated {target}")
    print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")


if __name__ == "__main__":
    main()
