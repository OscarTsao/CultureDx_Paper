from __future__ import annotations

from pathlib import Path


THESIS_PATHS = (
    Path("school/main.tex"),
    Path("paper/school/HiED_school_version.tex"),
)


def find_thesis() -> Path:
    matches = [path for path in THESIS_PATHS if path.exists()]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one thesis source, found: {matches}")
    return matches[0]


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    start_index = text.find(start)
    if start_index < 0:
        raise SystemExit(f"Start marker not found: {start}")
    if text.find(start, start_index + len(start)) >= 0:
        raise SystemExit(f"Start marker is not unique: {start}")
    end_index = text.find(end, start_index + len(start))
    if end_index < 0:
        raise SystemExit(f"End marker not found after {start}: {end}")
    return text[:start_index] + replacement.rstrip() + "\n" + text[end_index:]


CHINESE_ABSTRACT = r"""\chapter*{中文摘要}
\addcontentsline{toc}{chapter}{中文摘要}
精神科初診逐字稿中的鑑別診斷，需要在證據不完整下比較多個可能疾病，而非只辨識一個標籤。醫師需整合症狀、病程、時序、功能影響、排除病因與共病，但一次晤談未必能取得所有必要資訊。大型語言模型能整理候選診斷與證據，但流暢輸出不代表候選完整、準則判斷有逐字稿支持，或主診斷選擇恰當。只看最終準確率，也無法判斷分歧出現在哪個階段。

本研究提出 HiED，一套用於中文精神科逐字稿的混合式、以證據為基礎的多代理框架。診斷路徑透過相似案例檢索產生 Top-3 與初步主診斷；準則核對路徑使用 14 個診斷類別專屬的 Criterion Checker，將準則判定為符合、不符合或資訊不足，並形成準則相容集合。HiED 保存這些輸出，分別評估候選覆蓋、準則相容與主診斷選擇。

在固定的 1,000 例 LingxiDiag-16K 內部保留測試集上，HiED 的 Top-1 Accuracy 為 51.8\%，Top-3 Accuracy 為 80.2\%。其 Top-1 與 Single LLM 幾乎相同；TF--IDF 加邏輯迴歸在同來源資料上較強，但跨來源時明顯下降。最大分歧類型為參考診斷已進入 Top-3 並通過準則核對，卻未被選為最終主診斷；在可進行準則分析的案例中，此類型占內部案例的 29.7\%，在 MDD-5k 中占 25.6\%。所測試的主診斷選擇方法均未明確優於 Direct-Answer。

HiED 並未證明最終診斷準確率較高。其主要貢獻是提出可稽核的雙路徑架構與分階段評估框架，使候選遺漏、準則不相容、資訊不足與主診斷選擇分歧能在同一病例中分別檢視。所有結果皆來自合成中文逐字稿，不構成臨床驗證。

\noindent\textbf{關鍵詞：}大型語言模型、多代理系統、精神科鑑別診斷、診斷準則、臨床決策支援、可稽核人工智慧
"""

ENGLISH_ABSTRACT = r"""\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
Psychiatric differential diagnosis from a first-interview transcript requires comparing plausible disorders under incomplete evidence rather than assigning one label. Clinicians must integrate symptoms, course, timing, impairment, exclusionary causes, and comorbidity, but one interview may not provide all necessary information. Large language models can organize candidate diagnoses and evidence, but fluent output does not guarantee complete candidates, transcript-grounded criterion judgments, or appropriate primary-diagnosis selection. Final accuracy alone cannot show where disagreement appears.

This thesis proposes HiED, a hybrid, evidence-grounded multi-agent framework for Chinese psychiatric transcripts. The diagnosis path retrieves similar cases and produces a Top-3 list and a proposed primary diagnosis. The criterion-checking path uses fourteen diagnosis-specific Criterion Checkers to label criteria as met, not met, or insufficient evidence and form a criterion-compatible set. HiED preserves these outputs and separately evaluates candidate coverage, criterion compatibility, and primary-diagnosis selection.

On a fixed 1,000-case LingxiDiag-16K held-out set, HiED achieved 51.8\% Top-1 Accuracy and 80.2\% Top-3 Accuracy. Its Top-1 was almost identical to that of the Single LLM, while TF--IDF with logistic regression was stronger on same-source data but declined across sources. The largest disagreement group contained cases in which a reference diagnosis appeared in the Top-3 and passed criterion checking but was not selected as the final primary diagnosis. Among cases available for criterion analysis, this group accounted for 29.7\% internally and 25.6\% on MDD-5k. None of the tested primary-diagnosis selection methods clearly improved over Direct-Answer.

HiED does not establish superior final-diagnosis accuracy. Its main contribution is an auditable two-path architecture and stage-wise evaluation framework that makes candidate omission, criterion incompatibility, missing information, and primary-diagnosis selection disagreement separately inspectable for the same case. All results come from synthetic Chinese transcripts and do not constitute clinical validation.

\noindent\textbf{Keywords:} Large language models, multi-agent systems, psychiatric differential diagnosis, diagnostic criteria, clinical decision support, auditable AI
"""

METRIC_SECTION = r"""\section{Prediction Views and Metrics}
\label{sec:prediction-metrics}

The evaluator keeps four output views separate:

\begin{enumerate}[label=(\arabic*)]
\item The \emph{primary view}, $p_1(x)$, is the final primary diagnosis.
\item The \emph{ranked view}, $R_3(x)$, contains the first three distinct parent labels in a method's ranked output. TF--IDF with logistic regression obtains this view from ranked class scores. HiED obtains it from the Diagnostician ranking before DA or NtS finalization. A method that does not produce a ranked diagnostic list has no $R_3(x)$ view.
\item The \emph{compatibility view}, $L(x)$, is the set of scoring parent labels classified as criterion-compatible by the Compatibility Auditor under the configured study rules.
\item The \emph{multilabel view}, $M(x)$, is the complete set of emitted parent labels used for Exact Match and F1. For DA, it contains the final primary diagnosis and any emitted comorbid parent label. For a single-label method, it contains one label.
\end{enumerate}

Top-3 Accuracy is reported only for methods that produce a ranked diagnostic list. TF--IDF with logistic regression forms this list from its class scores, while HiED uses the Diagnostician ranking. Single does not provide the same ranked differential diagnosis, so no Top-3 Accuracy is reported for Single. The Majority baseline also has no Top-3 value. Their additional or single-label outputs remain part of the complete diagnosis set used for Exact Match and F1 where applicable.

Because a case may contain more than one gold label, Top-1 and Top-3 each count a case as correct when at least one projected benchmark gold label appears in the evaluated view. Exact Match, also called subset accuracy, instead requires the complete predicted label set to equal the complete gold-label set. These are benchmark-agreement measures, not independent measures of the patient's true clinical diagnosis.

For example, suppose that the projected gold-label set contains F41, while a ranked output places F32 first and F41.1 second. Because F41.1 is projected to its scoring parent F41, the case is incorrect under Top-1 evaluation but correct under Top-3 evaluation.

DA may emit a final primary diagnosis and one optional comorbid diagnosis, whereas NtS emits one reselected primary diagnosis. Their Top-1 comparison therefore evaluates the primary diagnosis directly, but differences in Exact Match, Macro-F1, or Weighted-F1 also reflect output cardinality and cannot be interpreted as isolated effects of primary re-selection.

Table~\ref{tab:metric-contract} summarizes which output view is evaluated by each measure. The subsequent equations give the case-level definitions used by the scoring implementation.

\begin{table}[H]
\centering
\caption{Definitions of the main evaluation measures by output view.}
\label{tab:metric-contract}
\small
\begin{tabularx}{\textwidth}{|>{\raggedright\arraybackslash}p{3.2cm}|>{\raggedright\arraybackslash}p{3.8cm}|>{\raggedright\arraybackslash}X|}
\hline
Measure & Evaluated output & Definition\\
\hline
Top-1 Accuracy & Final primary diagnosis, $p_1(x)$ & $p_1(x)\in G(x)$\\
\hline
Top-3 Accuracy & Ranked candidates, $R_3(x)$ & $R_3(x)\cap G(x)\neq\varnothing$\\
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

Top-1 and Top-3 Accuracy are computed over all evaluation cases. Top-3 Accuracy is reported only for a method with a ranked diagnostic list. Gold-label inclusion in the criterion-compatible set is computed over the cases with at least one non-\emph{Others} gold parent covered by a corresponding Criterion Checker.

\[
\mathrm{Top\text{-}1\ Accuracy}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[p_1(x)\in G(x)],
\]
\[
\mathrm{Top\text{-}3\ Accuracy}=\frac{1}{N}\sum_{x=1}^{N}\mathbb{1}[R_3(x)\cap G(x)\neq\varnothing],
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
This zero case matches the scoring implementation's \texttt{zero\_division=0} setting: a class with no positive support and no positive prediction contributes zero rather than being removed from the fixed class universe. Macro-F1 and Weighted-F1 are then
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

The 1,000-case output of the validation-selected HiED--DA parent-balanced configuration was independently rescored using the definitions above. The recalculation produced Top-1 Accuracy 0.518000, Top-3 Accuracy 0.802000, Exact Match 0.409000, Macro-F1 0.177577, and Weighted-F1 0.433738. These values reproduce the reported three-decimal results of 0.518, 0.802, 0.409, 0.178, and 0.434.

The same audit found a mean gold-set size of 1.093 and a mean predicted-set size of 1.136. HiED--DA emitted one diagnosis for 864 cases and two diagnoses for 136 cases. These counts confirm that Exact Match, Macro-F1, and Weighted-F1 in the main table are complete-set measures rather than primary-only measures. Primary-only F1 was also calculated as an exploratory check, but it is not substituted for the prespecified set-based F1 values.

For Majority, TF--IDF with logistic regression, and the validation-selected Single Global Top-5 configuration, only the retained aggregate headline results are used in this thesis. The available records do not support new paired case-level, output-overlap, or output-cardinality claims for those rows.

First-listed-label agreement compares the final primary diagnosis only with the first-listed projected gold parent. It is used for the confusion matrix but not for the main result. It may differ from any-gold Top-1 Accuracy when a case contains more than one gold parent label.

"""


def main() -> None:
    thesis_path = find_thesis()
    original = thesis_path.read_text(encoding="utf-8")
    updated = replace_between(
        original,
        r"\chapter*{中文摘要}",
        r"\chapter*{Abstract}",
        CHINESE_ABSTRACT,
    )
    updated = replace_between(
        updated,
        r"\chapter*{Abstract}",
        r"\chapter*{Acknowledgements}",
        ENGLISH_ABSTRACT,
    )
    updated = replace_between(
        updated,
        r"\section{Prediction Views and Metrics}",
        r"\section{Case-Level Indicators for Disagreement Localization}",
        METRIC_SECTION,
    )

    forbidden = (
        "emitted-label hit@3",
        "Emitted-label hit@3",
        r"E_3(x)",
        "Ranked Top-3 Accuracy",
        "genuine ranked Top-3 Accuracy",
        "分階段輸出與評估契約",
        "output and evaluation contract",
    )
    for term in forbidden:
        if term in updated:
            raise SystemExit(f"Forbidden legacy term remains: {term}")

    required = (
        "HiED 的 Top-1 Accuracy 為 51.8\\%，Top-3 Accuracy 為 80.2\\%。",
        "HiED achieved 51.8\\% Top-1 Accuracy and 80.2\\% Top-3 Accuracy.",
        "Top-3 Accuracy is reported only for methods that produce a ranked diagnostic list.",
        r"\mathrm{Top\text{-}3\ Accuracy}",
        "All results come from synthetic Chinese transcripts and do not constitute clinical validation.",
    )
    for term in required:
        if term not in updated:
            raise SystemExit(f"Required revised content missing: {term}")

    if updated == original:
        raise SystemExit("Patch made no changes")

    thesis_path.write_text(updated, encoding="utf-8")
    print(f"Updated {thesis_path}")


if __name__ == "__main__":
    main()
