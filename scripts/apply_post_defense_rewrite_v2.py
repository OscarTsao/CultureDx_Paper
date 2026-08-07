from __future__ import annotations

import re
from pathlib import Path


ZH_ABSTRACT = r"""精神科初診逐字稿中的鑑別診斷，是在資訊不完整的情況下比較多個可能診斷的過程。同一份逐字稿可能同時支持多個疾病，但醫師仍需根據目前取得的資訊選擇一個主診斷。影響判斷的重要資訊，例如症狀持續時間、症狀出現的先後、病程變化、其他可能病因與共病關係，未必能在一次初診中完整取得。大型語言模型可以閱讀醫病對話並產生診斷結果，但一個看似合理的答案不代表診斷過程可以被檢查與分析。

現有精神科大型語言模型研究多以最終診斷準確率評估系統。然而，單一最終答案無法說明分歧發生在哪個階段。資料集標準答案可能沒有進入候選名單，可能進入候選但未通過準則核對，也可能已經同時出現在候選名單與準則相容集合中，最後卻沒有被選為主診斷。這些情況需要不同的改善方式，但只看最終準確率時會被混在一起。

本研究提出 HiED，一套面向中文精神科初診逐字稿的分階段決策支援架構。HiED 將診斷流程分為候選形成、準則核對與主診斷選擇三個階段，並使用兩條互補路徑保留不同資訊。診斷路徑產生排序後的候選診斷與建議主診斷；準則驗證路徑則檢查各診斷的準則，並將每一項標記為符合、不符合或資訊不足。系統另外保留準則相容集合與最後的選擇結果，使各階段可以分開分析。

在 LingxiDiag-16K 內部測試集上，HiED 的 Top-1 Accuracy 為 51.8\%，genuine Top-3 Accuracy 為 80.2\%。TF--IDF 加邏輯迴歸在同一語料內的標籤預測表現較高，但跨語料測試時表現明顯下降，也不提供逐項準則狀態或診斷階段紀錄。在 915 個可進行準則分析的案例中，有 272 例（29.7\%）的資料集標準答案已進入前三個候選，也通過準則相容檢查，但最後未被選為主診斷。MDD-5k 的 878 個可分析案例中，也有 225 例（25.6\%）出現相同的主診斷選擇分歧。

本研究的第一項貢獻，是提出一個能分別記錄與分析候選形成、準則核對與主診斷選擇的架構，並透過這個架構找出主診斷選擇是兩個合成資料集中的最大已記錄分歧類型。第二項貢獻，是提供排序後的候選診斷、逐項準則狀態、準則相容集合與資訊不足項目，供醫師篩選可能診斷與檢查仍需補充的資訊。HiED 的目的不是取代醫師，而是提供比單一診斷標籤更多的決策支援資訊。目前量化結果來自合成中文逐字稿；本論文唯一保留的臨床人員評估，是針對部分 LingxiDiag 案例進行的盲性精神科醫師標注。真實病人臨床評估不在本論文範圍內。"""


EN_ABSTRACT = r"""Differential diagnosis from a first psychiatric interview transcript requires comparing several possible disorders with incomplete information. Several disorders may fit the same transcript, but a clinician still needs to choose a primary diagnosis. Important facts, such as how long symptoms have lasted, which symptoms started first, how the condition has changed, other possible causes, and comorbidity, may be missing from one visit. Large language models can read these conversations and produce diagnoses, but a reasonable answer does not make the diagnostic process visible.

Most psychiatric LLM studies report final diagnosis accuracy. However, one final answer does not show where a disagreement occurs. A dataset reference diagnosis may be missing from the candidate list, may enter the list but fail the criterion check, or may appear in both the candidate list and the criterion-compatible set but still not be selected as primary. These cases need different improvements, but one final accuracy score combines them.

We propose HiED, a stage-wise decision-support framework for Chinese psychiatric interview transcripts. HiED separates the task into candidate generation, criterion checking, and primary diagnosis selection. It uses two complementary paths. The diagnosis path returns ranked candidate diagnoses and a proposed primary diagnosis. The criterion path checks each configured diagnosis and marks each criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. The system also keeps the criterion-compatible set and the final selection so that each stage can be studied separately.

On the LingxiDiag-16K internal test set, HiED achieved 51.8\% Top-1 Accuracy and 80.2\% genuine Top-3 Accuracy. TF--IDF with logistic regression gave stronger label prediction when training and test data came from the same corpus, but its performance dropped when the corpus changed. It also did not provide criterion states or a record of the diagnostic stages. Among 915 internal cases available for criterion analysis, 272 cases (29.7\%) contained a dataset reference diagnosis in both the Top-3 and the criterion-compatible set, but another diagnosis was selected as primary. The same pattern appeared in 225 of 878 external MDD-5k cases (25.6\%).

The first contribution of this thesis is an architecture that records and evaluates candidate generation, criterion checking, and primary diagnosis selection separately. This architecture shows that primary diagnosis selection is the largest recorded disagreement group in the two tested synthetic datasets. The second contribution is the structured information provided for clinical review: ranked candidates, criterion states, the criterion-compatible set, and missing information. These outputs are designed to help clinicians screen possible diagnoses and decide what information still needs to be collected. HiED is designed to support clinicians, not replace them. The quantitative results use synthetic Chinese transcripts. The only clinician-facing evaluation kept in this thesis is a blinded psychiatrist annotation study on selected LingxiDiag cases; real-patient clinical evaluation is outside the scope of this thesis."""


CHAPTER_ONE = r"""\section{Background and Motivation}

Psychiatric outpatient care is easy to access in Taiwan, but large hospitals also face a heavy workload. During a first psychiatric visit, the clinician must collect the patient's history, understand the current symptoms, observe the mental state, check immediate risks, and form an initial diagnosis within limited time. Important facts may still be missing, such as when the symptoms began, how long they have lasted, how they have changed, and whether another cause may explain them~\citep{lin2020outpatient}.

Patients may also describe emotional distress through everyday or physical complaints. In Chinese-speaking settings, they may first report poor sleep, fatigue, dizziness, chest tightness, or stomach problems instead of saying that they feel depressed or anxious~\citep{kleinman1982neurasthenia,ryder2008somatic}. The same symptom may also be described in different ways. The clinician must therefore turn a free-form conversation into clinical evidence while keeping the full context of the interview in view.

This task is difficult because common mental disorders share many symptoms. Depression, anxiety, stress-related disorders, obsessive-compulsive disorder, somatic symptom disorders, and sleep disorders may all involve poor sleep, fatigue, poor concentration, and reduced daily function. A diagnosis cannot be made from one symptom alone. Each disorder has its own rules for key symptoms, symptom count, duration, effects on daily life, and the exclusion of other causes~\citep{who2019icd10}.

Even after these rules are checked, more than one diagnosis may still fit the same transcript. The symptoms may come from one main disorder, or more than one disorder may be present at the same time. This second case is called comorbidity~\citep{brown2001comorbidity}. In other cases, the available information may not be enough to choose one clear primary diagnosis. Structured diagnostic studies also report limited agreement for some common disorders~\citep{regier2013dsm5}.

A first psychiatric visit is therefore a comparison among possible diagnoses under incomplete evidence. It includes three linked decisions: forming a list of possible diagnoses, checking whether the available evidence meets the diagnostic criteria, and selecting a primary diagnosis while also considering possible comorbidities. A mistake or uncertainty can appear at any of these steps. Time pressure may also increase the risk of focusing too early on one diagnosis~\citep{croskerry2003cognitive}.

For this reason, a useful decision-support system should provide more information than one final diagnosis. It should show the ranked candidate diagnoses, the state of each diagnostic criterion, and the information that is still missing. These outputs are designed to help clinicians review the case, narrow the candidate list, and decide what should be checked next.

\section{Problem Definition and Challenges}
\label{sec:problem-definition}

Large language models can process clinical dialogue and produce diagnostic outputs. Medical multi-agent systems can also assign different tasks to different model calls and combine their outputs~\citep{li2024taiwan,raballo2025,sarma2025,tang2024medagents,kim2024mdagents}. These methods are useful for psychiatric transcript analysis, but a final diagnosis alone does not show how the result was formed or where a disagreement occurred.

A final disagreement can start at different stages. A dataset reference diagnosis may never enter the candidate list. It may enter the list but fail the criterion check. It may also appear in both the candidate list and the criterion-compatible set, but another diagnosis may still be selected as primary. These cases need different improvements, but one final accuracy score groups them together.

In this thesis, a benchmark or dataset reference label is a diagnosis supplied by the dataset for scoring. It is not an independently reviewed clinical diagnosis. The recorded outputs therefore show where HiED agrees or disagrees with the benchmark; they do not by themselves show which diagnosis is clinically correct.

A high final accuracy score also needs careful interpretation. A text classifier may learn words and label patterns that are common in one corpus. It may score well when its training and test cases come from the same source, but its performance may fall when the data source changes. Same-corpus label prediction, cross-corpus transfer, and the amount of information provided for clinical review are different questions.

The main technical problem studied in this thesis is how to make the three diagnostic decisions separately visible. This allows us to identify whether a benchmark disagreement appears during candidate generation, criterion checking, or primary diagnosis selection. Cross-corpus testing is used as an additional boundary analysis rather than as the main contribution of HiED.

\section{Overview of HiED and Study Scope}

A Single LLM baseline reads a fixed transcript and directly returns a primary diagnosis. It may also return a comorbid diagnosis. However, it does not follow the same output contract as HiED: it does not provide the same genuine ranked candidate list or an independent criterion-level record for every configured diagnosis. Its output is therefore mainly used to evaluate the final diagnostic result.

This thesis proposes HiED, a hybrid, evidence-grounded multi-agent decision-support framework for Chinese psychiatric interview transcripts. HiED uses two connected paths. The diagnosis path ranks possible diagnoses and proposes a primary diagnosis. The criterion path checks every configured diagnosis against study-specific criteria informed by ICD-10. Each criterion is marked as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}.

A Compatibility Auditor then forms the criterion-compatible set, and a finalization policy records the committed primary diagnosis. All methods in this study receive a fixed transcript and cannot ask the patient follow-up questions. The two paths therefore examine the same available evidence from different views.

HiED keeps the ranked candidate list, model-generated criterion states, supporting text, criterion-compatible set, and final selection as separate outputs. These records support two uses. First, they allow candidate generation, criterion checking, and primary diagnosis selection to be studied separately. Second, they provide structured information for clinical review. A clinician can inspect the possible diagnoses, check which criteria are supported or contradicted, and see which information is still missing.

In this thesis, \emph{auditable} means that these outputs are kept and can be checked after the system finishes. It does not mean that the criterion states, supporting text, compatible diagnoses, or final diagnosis are clinically correct. These outputs remain model-generated records until they are reviewed by clinicians.

HiED is motivated by Chinese-language psychiatric care in the Taiwanese outpatient setting. The completed quantitative experiments use synthetic Chinese dialogue datasets. The only clinician-facing evaluation kept in this thesis is a blinded psychiatrist annotation study on selected LingxiDiag cases. Real-patient clinical evaluation is outside the scope of this thesis. HiED is designed to support clinical review, not to replace the clinician.

\section{Contributions}

This thesis makes two main contributions.

First, it presents a two-path and stage-wise architecture for psychiatric decision support. Compared with a Single LLM that mainly returns a final diagnostic output, HiED separately records the ranked candidate list, criterion-checking results, criterion-compatible set, and committed primary diagnosis. This design allows candidate generation, criterion checking, and primary diagnosis selection to be studied separately. Using these outputs, this thesis finds that primary diagnosis selection is the largest recorded disagreement group in the two tested synthetic datasets. This is a benchmark finding under the evaluated settings, not a claim about the true clinical primary diagnosis in every case.

Second, HiED provides structured diagnostic information for clinical review instead of only one final diagnosis. It returns ranked possible diagnoses and marks each diagnostic criterion as \texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}. It also keeps the criterion-compatible set and the final selection record. These outputs are designed to help clinicians screen possible diagnoses, review supporting or conflicting evidence, and identify what information is still missing. Their effect on clinical speed, accuracy, and safety still requires direct clinical evaluation.

\section{Thesis Organization}

Chapter~\ref{ch:related} reviews related work on psychiatric large language models, medical multi-agent systems, criterion-based diagnosis, and auditable decision support. Chapter~\ref{ch:architecture} compares the Single LLM and HiED study architectures and follows a complete transcript through the recorded outputs. Chapter~\ref{ch:data} defines the datasets, label mapping, output views, evaluation measures, and statistical methods. Chapter~\ref{ch:experimental} describes retrieval settings, primary diagnosis selection methods, external synthetic evaluation, and the LingxiDiag psychiatrist annotation study. Chapters~\ref{ch:results} and~\ref{ch:external} report the internal and external synthetic results. Chapter~\ref{ch:error} examines the main recorded disagreement patterns. Chapters~\ref{ch:discussion}--\ref{ch:conclusion} discuss the findings, limitations, conclusions, and future work."""


RQ_BLOCK = r"""\begin{description}[style=nextline,leftmargin=1.5cm,labelwidth=1.1cm,itemsep=0pt,parsep=0pt,topsep=0pt,partopsep=0pt]
\item[RQ1] How does HiED perform compared with conventional classification methods and Single LLM baselines under the same evaluation settings?
\item[RQ2] Where do benchmark disagreements occur across candidate generation, criterion checking, and primary diagnosis selection?
\item[RQ3] How do different similar-case retrieval strategies affect diagnostic outputs in Single LLM and HiED?
\item[RQ4] Can alternative primary diagnosis selection strategies reduce selection disagreement after candidate generation and criterion checking?
\item[RQ5] Do the observed stage-wise disagreement patterns remain under another synthetic dataset and different diagnostic settings?
\end{description}"""


CONCLUSION = r"""\chapter{Conclusions and Future Work}
\label{ch:conclusion}

\section{Summary of Findings}

This thesis proposed HiED, a stage-wise decision-support framework for psychiatric differential diagnosis from Chinese interview transcripts. Instead of treating diagnosis as one classification output, HiED separates candidate generation, criterion checking, and primary diagnosis selection. It keeps ranked candidate diagnoses, criterion states, the criterion-compatible set, and the committed diagnosis as separate outputs.

The main value of HiED is not only its final prediction. The recorded outputs also show where a benchmark disagreement appears. On the internal synthetic benchmark, many dataset reference diagnoses were already present in the candidate list and passed the criterion-compatible check. The largest recorded disagreement group appeared at primary diagnosis selection: 272 of 915 checker-eligible cases contained a reference diagnosis in both the Top-3 and the criterion-compatible set, but another diagnosis was selected as primary.

The tested selection methods did not consistently improve committed-primary agreement. The same broad pattern also appeared on MDD-5k, where 225 of 878 checker-eligible cases were ranked and criterion-compatible but not selected. These results show a repeated benchmark pattern across two synthetic datasets. They do not show that the dataset label is the only clinically correct diagnosis or that primary selection is the main difficulty in all clinical settings.

Beyond the final diagnosis, HiED provides structured information for review. Ranked candidates, criterion states, compatible diagnoses, and missing information can help a clinician inspect possible diagnoses and decide what should be checked next. HiED is therefore designed as a decision-support framework rather than an autonomous diagnostic system.

\section{Answers to the Research Questions}

The answers below are limited to the tested synthetic datasets, label mappings, and recorded system outputs.

\begin{description}[style=nextline,leftmargin=1.5cm,labelwidth=1.1cm,itemsep=0.2em,parsep=0pt]

\item[RQ1] \textbf{How does HiED perform compared with conventional classification methods and Single LLM baselines under the same evaluation settings?}

TF--IDF with logistic regression achieved the strongest same-corpus label prediction on the internal test set. Single LLM and HiED had similar committed-primary Top-1 values. HiED did not provide an overall accuracy advantage, but it provided a genuine ranked differential, criterion states, a criterion-compatible set, and a final selection record that supported stage-wise analysis.

\item[RQ2] \textbf{Where do benchmark disagreements occur across candidate generation, criterion checking, and primary diagnosis selection?}

The largest recorded disagreement group occurred after candidate generation and criterion checking. Among 915 checker-eligible internal cases, 272 contained a dataset reference diagnosis in both the genuine Top-3 and the criterion-compatible set, but another diagnosis was selected as primary. This result identifies primary diagnosis selection as the main recorded bottleneck under the tested HiED setting.

\item[RQ3] \textbf{How do different similar-case retrieval strategies affect diagnostic outputs in Single LLM and HiED?}

Retrieval gave a clearer benefit for Single LLM than for HiED. Global Top-5 retrieval improved the Single baseline over no retrieval. For HiED, the differences among no retrieval, global Top-5, and parent-balanced retrieval were smaller and did not show a stable gain for one retrieval setting across the reported comparisons.

\item[RQ4] \textbf{Can alternative primary diagnosis selection strategies reduce selection disagreement after candidate generation and criterion checking?}

None of the tested methods gave a clear and stable improvement over Direct-Answer. Criterion-based re-selection reduced Top-1 under all three internal retrieval settings, and the other tested rules, comparisons, debate, and repeated sampling also did not consistently close the selection gap. These results apply to the tested methods and do not rule out other selection designs.

\item[RQ5] \textbf{Do the observed stage-wise disagreement patterns remain under another synthetic dataset and different diagnostic settings?}

The broad pattern appeared again on MDD-5k: candidate coverage and criterion inclusion were higher than committed-primary agreement, and the largest disagreement group again contained a reference diagnosis that was ranked and criterion-compatible but not selected. The group proportions were not identical, and the result remains limited to synthetic data.

\end{description}

\section{Future Work}

\paragraph{Complete the LingxiDiag psychiatrist annotation study.}

The next clinical-facing step is the blinded psychiatrist annotation of selected LingxiDiag disagreement cases. Psychiatrists will judge whether each transcript supports one primary diagnosis or remains insufficient, rank possible diagnoses, and mark the relevant criterion states. This study can compare psychiatrist judgments with the dataset labels and HiED outputs without treating either source as automatic clinical truth. Real-patient clinical evaluation is outside the scope of this thesis.

\paragraph{Model comparative primary diagnosis selection.}

The current criterion path mainly asks whether each diagnosis is compatible with the transcript. It does not fully represent why one compatible diagnosis should be selected before another. Future methods should model direct relations among candidates, including which symptoms started first, illness course, episode structure, other possible causes, comorbidity, and which diagnosis best explains the available evidence.

\paragraph{Ask for missing evidence.}

A fixed transcript may not contain enough information to separate the leading diagnoses. Future decision-support systems should identify the unresolved difference and suggest targeted follow-up questions about duration, timing, previous episodes, substance use, medical causes, and effects on daily life. When the missing information cannot be obtained, the system should also support an explicit insufficient-information outcome instead of forcing one primary diagnosis.

HiED shows that candidate availability and criterion compatibility do not always lead to committed-primary benchmark agreement. Its current contribution is to make this gap visible and to provide structured information for review. Better comparative selection and clinical assessment of the recorded outputs remain the main directions for future work."""


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


def replace_first_description_after(text: str, anchor: str, block: str) -> str:
    anchor_index = text.index(anchor)
    start = text.index("\\begin{description}", anchor_index)
    end = text.index("\\end{description}", start) + len("\\end{description}")
    return text[:start] + block.strip() + text[end:]


def replace_section_body(text: str, section_marker: str, next_section_marker: str, body: str) -> str:
    start = text.index(section_marker) + len(section_marker)
    end = text.index(next_section_marker, start)
    return text[:start] + "\n\n" + body.strip() + "\n\n" + text[end:]


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
        "\\chapter{Related Work}",
        CHAPTER_ONE,
    )
    updated = replace_first_description_after(
        updated,
        "This thesis therefore uses five research questions:",
        RQ_BLOCK,
    )
    updated = replace_block(
        updated,
        "\\chapter{Conclusions and Future Work}",
        "\\appendix",
        CONCLUSION,
    )

    # Keep the clinical scope limited to the LingxiDiag psychiatrist annotation study.
    updated = updated.replace(
        "\\section{Complementary Clinical Evaluation Plan}",
        "\\section{LingxiDiag Psychiatrist Annotation Study}",
    )
    updated = updated.replace(
        "\\subsection{LingxiDiag Pilot Psychiatrist Review}\n",
        "",
    )
    cgmh_start = "\\subsection{Ongoing CGMH Real-World Validation}"
    if cgmh_start in updated:
        start = updated.index(cgmh_start)
        end = updated.index("\\chapter{Internal Evaluation Results}", start)
        updated = updated[:start] + updated[end:]

    updated = replace_section_body(
        updated,
        "\\section{Evaluation Overview}\n\\label{sec:experimental-overview}",
        "\\section{Retrieval-Configuration Selection and Benchmark Positioning}",
        "The completed computational study includes validation-based retrieval selection, internal benchmark comparison, stage-wise disagreement analysis, primary-selection interventions, and external synthetic evaluation. These analyses use fixed transcript inputs and do not include real-patient data. A separate blinded psychiatrist annotation study on selected LingxiDiag cases is described at the end of this chapter.",
    )

    updated = re.sub(
        r"The blinded LingxiDiag pilot and CGMH real-world validation described in Section~\\ref\{sec:clinical-evaluation-plan\} remain ongoing and contribute no completed clinical evidence to this thesis\..*?independent transcript-only reference assessments\.",
        "The blinded LingxiDiag psychiatrist annotation study described in Section~\\ref{sec:clinical-evaluation-plan} is the only clinician-facing evaluation included in this thesis. Until completed, it contributes no clinical outcome evidence. The study uses a selected synthetic disagreement sample rather than a representative clinical population.",
        updated,
        flags=re.DOTALL,
    )

    updated = re.sub(
        r"and the protocol for the ongoing CGMH real-world validation study\.",
        "and the design of the psychiatrist annotation study for selected LingxiDiag cases.",
        updated,
    )
    updated = re.sub(
        r"I thank the clinical team of the Division of Psychosomatic Medicine at\nChang Gung Memorial Hospital for their collaboration on the study\nprotocol and clinical review\.",
        "I thank the clinical team of the Division of Psychosomatic Medicine at\nChang Gung Memorial Hospital for their clinical feedback and helpful\ndiscussions.",
        updated,
    )
    updated = updated.replace(
        "CGMH & Chang Gung Memorial Hospital\\\\\n\\hline\n",
        "",
    )

    if (updated.count("\\ct{"), updated.count("\\wl{")) != comment_counts:
        raise RuntimeError("Advisor comment counts changed unexpectedly")
    if "\\showcommentstrue" not in updated:
        raise RuntimeError("Advisor-comment display guard was removed")
    if "Ongoing CGMH Real-World Validation" in updated or "ongoing CGMH" in updated:
        raise RuntimeError("Obsolete CGMH evaluation text remains")
    if "stage-wise decision-support framework" not in updated:
        raise RuntimeError("New thesis positioning was not applied")
    if "272 cases (29.7\\%)" not in updated:
        raise RuntimeError("Core stage-wise result is missing")

    target.write_text(updated, encoding="utf-8")
    print(f"Updated {target}")
    print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")


if __name__ == "__main__":
    main()
