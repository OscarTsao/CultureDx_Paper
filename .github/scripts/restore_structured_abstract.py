from __future__ import annotations

import os
from pathlib import Path


if os.environ.get("GITHUB_REPOSITORY") == "OscarTsao/CultureDx_Paper":
    target = Path("school/main.tex")
else:
    target = Path("paper/school/HiED_school_version.tex")

text = target.read_text(encoding="utf-8")
start_marker = r"\chapter*{中文摘要}"
end_marker = r"\chapter*{Acknowledgements}"
if text.count(start_marker) != 1 or text.count(end_marker) != 1:
    raise SystemExit("Abstract boundary markers are not unique")

abstract = r"""\chapter*{中文摘要}
\addcontentsline{toc}{chapter}{中文摘要}
精神科初診逐字稿的鑑別診斷，是在證據不完整下比較多個可能疾病，而非只辨識一個標籤。醫師需整理症狀、病程、時序、功能影響、排除病因與共病，但這些資訊未必能在一次晤談中完整取得。大型語言模型可整理候選診斷與證據，但流暢輸出不保證鑑別診斷完整、準則判斷有逐字稿支持，或主診斷選擇恰當。只看最終準確率也無法區分候選遺漏、準則不相容，或參考診斷已存在但未被確立為主診斷。

本研究提出 HiED，一套用於中文精神科初診逐字稿的混合式、以證據為基礎的多代理框架。其雙路徑分階段流程，結合透過相似案例檢索產生排序鑑別診斷的診斷路徑，以及 14 個診斷類別專屬的 Criterion Checker，將各項準則判定為符合、不符合或資訊不足。確定性規則據此形成準則相容集合，最後確立主診斷並可保留共病。HiED 保存同一病例的排序候選、準則狀態、證據說明、相容集合與最終輸出，使各階段能分開評估。

在固定的 1,000 例 LingxiDiag-16K 內部保留測試集上，HiED 的 committed Top-1 Accuracy 為 51.8\%，genuine ranked Top-3 Accuracy 為 80.2\%。其 Top-1 與直接 Single LLM 幾乎相同；TF--IDF 加邏輯迴歸在同來源評估中較強，但跨來源時明顯下降。在 915 個可進行準則分析的案例中，有 272 例（29.7\%）的參考診斷已同時進入 Top-3 與準則相容集合，卻未被確立為主診斷；MDD-5k 的 878 個可分析案例中，也有 225 例（25.6\%）出現相同型態。所測試的確定性、成對比較、辯論與重複生成策略，均未明確優於 Direct-Answer。

因此，HiED 並未證明最終標籤準確率較高。其主要貢獻是同病例的分階段輸出與評估契約，使候選遺漏、準則不相容、資訊不足及主診斷確立分歧可被分別檢視。本研究證據來自合成中文逐字稿，不構成臨床驗證；單一精神科醫師的基準標籤一致性審查列為後續工作。

\noindent\textbf{關鍵詞：}大型語言模型、多代理系統、精神科鑑別診斷、診斷準則、臨床決策支援、可稽核人工智慧
\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
Psychiatric differential diagnosis from a first-interview transcript requires comparing plausible disorders under incomplete evidence, not simply assigning one label. Clinicians must organize symptoms, course, timing, impairment, exclusionary causes, and comorbidity, but these details may not be fully elicited in one visit. Large language models can organize candidates and evidence; however, fluent output does not guarantee a complete differential, grounded criterion judgments, or appropriate primary selection. Final accuracy alone cannot localize candidate omission, criterion incompatibility, or disagreement after the reference diagnosis is already available.

This thesis proposes HiED, a hybrid, evidence-grounded multi-agent framework for Chinese psychiatric interview transcripts. Its two-path, stage-wise process combines a diagnostic path that retrieves similar cases and produces a ranked differential with fourteen diagnosis-specific Criterion Checkers that label criteria as met, not met, or insufficient evidence. Deterministic rules form a criterion-compatible set, and finalization commits a primary diagnosis and may retain a comorbidity. HiED preserves these same-case outputs for separate stage-wise evaluation.

On a fixed 1,000-case LingxiDiag-16K held-out set, HiED achieved 51.8\% committed Top-1 Accuracy and 80.2\% genuine ranked Top-3 Accuracy. Top-1 was almost identical to the direct Single LLM, whereas TF--IDF with logistic regression was stronger under same-source evaluation but declined substantially across sources. Among 915 checker-eligible LingxiDiag cases, 272 (29.7\%) contained a benchmark-reference diagnosis in both the Top-3 and criterion-compatible set, but no reference diagnosis was committed as primary. The same profile appeared in 225 of 878 MDD-5k cases (25.6\%). Tested deterministic, pairwise, debate, and repeated-generation strategies did not clearly improve on Direct-Answer.

HiED therefore does not establish superior final-label accuracy. Its main contribution is a same-case stage-wise output and evaluation contract that makes candidate omission, criterion incompatibility, missing information, and primary-commitment disagreement separately inspectable. The evidence comes from synthetic Chinese transcripts and is not clinical validation; a single-psychiatrist benchmark-label alignment review remains future work.

\noindent\textbf{Keywords:} Large language models, multi-agent systems, psychiatric differential diagnosis, diagnostic criteria, clinical decision support, auditable AI

"""

start = text.index(start_marker)
end = text.index(end_marker, start)
text = text[:start] + abstract + text[end:]

required = [
    "而非只辨識一個標籤",
    "混合式、以證據為基礎的多代理框架",
    "其雙路徑分階段流程",
    "所測試的確定性、成對比較、辯論與重複生成策略",
    "not simply assigning one label",
    "a hybrid, evidence-grounded multi-agent framework",
    "Its two-path, stage-wise process",
    "Tested deterministic, pairwise, debate, and repeated-generation strategies",
    "a single-psychiatrist benchmark-label alignment review remains future work.",
]
for item in required:
    if item not in text:
        raise SystemExit(f"Missing required abstract text: {item}")

forbidden = [
    "精神科初診逐字稿的鑑別診斷，需在資訊不完整下比較多個可能疾病並選擇主診斷。",
    "Differential diagnosis from a first psychiatric interview transcript requires comparing several possible disorders and choosing a primary diagnosis from incomplete information.",
    "A proposed single-psychiatrist benchmark-label alignment review with a blinded initial assessment is documented as future work",
]
for item in forbidden:
    if item in text:
        raise SystemExit(f"Legacy short abstract text remains: {item}")

if text.count(start_marker) != 1 or text.count(r"\chapter*{Abstract}") != 1:
    raise SystemExit("Abstract chapter count is not one")

target.write_text(text, encoding="utf-8")
print(f"updated {target}")
