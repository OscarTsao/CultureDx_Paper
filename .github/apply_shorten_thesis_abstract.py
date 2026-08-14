from __future__ import annotations

import re
import sys
from pathlib import Path


CHINESE_BODY = r"""精神科初診逐字稿的鑑別診斷，需在資訊不完整下比較多個可能疾病並選擇主診斷。症狀持續時間、出現順序、病程、排除病因與共病關係可能未被完整記錄。現有精神科大型語言模型研究多以最終診斷準確率評估，因而無法區分分歧是來自候選遺漏、準則不相容，或參考診斷已存在但未被選為主診斷。

本研究提出 HiED，一套用於中文精神科初診逐字稿的分階段決策支援架構。HiED 將流程分為候選形成、準則核對與主診斷選擇，並保留排序後的候選診斷、逐項準則狀態、準則相容集合與最後的主診斷，使各階段能被分開檢查與分析。

在 LingxiDiag-16K 內部測試集上，HiED 的 Top-1 Accuracy 為 51.8\%，genuine Top-3 Accuracy 為 80.2\%。TF--IDF 加邏輯迴歸在同語料內的標籤預測較強，但跨語料表現明顯下降，且不提供準則狀態或診斷階段紀錄。在 915 個可進行準則分析的案例中，有 272 例（29.7\%）的參考診斷已進入前三個候選並通過準則相容檢查，但沒有參考診斷被確立為主診斷；MDD-5k 的 878 個可分析案例中，也有 225 例（25.6\%）出現相同型態。

HiED 的主要貢獻，是將候選形成、準則核對與主診斷選擇分開記錄，並提供排序候選、準則狀態、資訊不足項目與最終選擇，讓診斷分歧與待補資訊可被檢視。HiED 旨在支援而非取代醫師。量化結果來自合成中文逐字稿；針對部分 LingxiDiag 案例的盲性精神科醫師標注仍待完成，真實病人評估不在本論文範圍內。

"""

ENGLISH_BODY = r"""Differential diagnosis from a first psychiatric interview transcript requires comparing several possible disorders and choosing a primary diagnosis from incomplete information. Important facts, including symptom duration, temporal order, illness course, exclusionary causes, and comorbidity, may be missing. Most psychiatric LLM studies report only final diagnosis accuracy and therefore cannot distinguish candidate omission, criterion incompatibility, and disagreement after a reference diagnosis is already available.

We propose HiED, a stage-wise decision-support framework for Chinese psychiatric interview transcripts. HiED separates candidate generation, criterion checking, and primary diagnosis selection. It records ranked candidates, criterion states, the criterion-compatible set, and the committed primary diagnosis so that each output stage can be examined separately.

On the LingxiDiag-16K internal test set, HiED achieved 51.8\% Top-1 Accuracy and 80.2\% genuine Top-3 Accuracy. TF--IDF with logistic regression provided stronger same-corpus label prediction, but its performance dropped substantially across corpora and it did not provide criterion states or stage-wise records. Among 915 internal cases available for criterion analysis, 272 cases (29.7\%) contained a reference diagnosis in both the Top-3 and the criterion-compatible set, but no reference diagnosis was committed as primary. The same pattern appeared in 225 of 878 MDD-5k cases (25.6\%).

HiED's main contribution is to record candidate generation, criterion checking, and primary commitment separately while providing ranked alternatives, criterion states, missing-information records, and the final decision for review. It is designed to support, not replace, clinicians. The quantitative evidence comes from synthetic Chinese transcripts. A blinded psychiatrist annotation study on selected LingxiDiag cases remains pending, and real-patient evaluation is outside the scope of this thesis.

"""


def replace_between(text: str, start_marker: str, end_marker: str, body: str, label: str) -> str:
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise RuntimeError(f"{label}: expected unique markers")
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + body + text[end:]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_shorten_thesis_abstract.py TARGET_TEX")

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    text = replace_between(
        text,
        "\\chapter*{中文摘要}\n\\addcontentsline{toc}{chapter}{中文摘要}\n",
        "\\noindent\\textbf{關鍵詞：}",
        CHINESE_BODY,
        "Chinese abstract",
    )
    text = replace_between(
        text,
        "\\chapter*{Abstract}\n\\addcontentsline{toc}{chapter}{Abstract}\n",
        "\\noindent\\textbf{Keywords:}",
        ENGLISH_BODY,
        "English abstract",
    )

    english_words = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", ENGLISH_BODY))
    chinese_nonspace = len(re.sub(r"\s+", "", CHINESE_BODY))
    if english_words > 270:
        raise RuntimeError(f"English abstract remains too long: {english_words} words")
    if chinese_nonspace > 650:
        raise RuntimeError(f"Chinese abstract remains too long: {chinese_nonspace} non-space characters")

    path.write_text(text, encoding="utf-8")
    print(
        f"Updated {path}: Chinese={chinese_nonspace} non-space characters; "
        f"English={english_words} words"
    )


if __name__ == "__main__":
    main()
