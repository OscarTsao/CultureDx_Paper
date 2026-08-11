from __future__ import annotations

from pathlib import Path
import sys

TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("school/main.tex")

CHINESE_ABSTRACT = r"""\chapter*{中文摘要}
\addcontentsline{toc}{chapter}{中文摘要}
精神科初診的鑑別診斷，需要在資訊不完整時比較多個可能疾病。症狀持續時間、出現先後、病程、排除性病因與共病等關鍵資訊，未必能在一次晤談中取得。許多精神科大型語言模型系統以產生最終診斷為主要目標，再透過解釋提高預測結果的可理解性。這類設計仍以診斷預測為中心，較少直接支援醫師比較候選診斷與辨識缺失資訊。

本研究提出 HiED，一套面向中文精神科逐字稿的分階段決策支援架構。HiED 將流程分為候選形成、準則核對與主診斷選擇，並保留排序後的候選診斷、準則狀態（符合、不符合或資訊不足）、準則相容集合與最終選擇結果。

分階段分析顯示，兩個資料集中最多的已記錄分歧都出現在主診斷選擇階段。LingxiDiag-16K 有 272 例，MDD-5k 有 225 例。在這些案例中，至少一個資料集標準答案已進入前三個候選，也位於準則相容集合中，但系統最後仍選擇了另一個主診斷。我們測試的重新選擇方法也沒有帶來明確改善。

因此，HiED 的主要貢獻不是提高診斷準確率，而是提供一份可供檢視的結構化紀錄，協助醫師快速篩選候選診斷、定位相關症狀與準則證據，並找出仍需補充的資訊。HiED 是決策支援研究架構，而非自主診斷系統。本研究量化評估使用合成中文逐字稿，真實病人評估不在本論文範圍內。

\noindent\textbf{關鍵詞：}大型語言模型、多代理系統、精神科鑑別診斷、臨床決策支援、ICD-10、可稽核人工智慧
"""

ENGLISH_ABSTRACT = r"""\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
Psychiatric differential diagnosis from a first interview requires comparing several disorders with incomplete information. Key facts, such as symptom duration, temporal order, illness course, exclusionary causes, and comorbidity, may be missing. Many psychiatric LLM systems are diagnosis-centered: they mainly produce a final diagnosis, while explanations are used to make that prediction easier to interpret. This design gives limited support for clinicians who need to compare alternatives and identify missing evidence.

We propose HiED, a stage-wise decision-support framework for Chinese psychiatric interview transcripts. HiED separates candidate generation, criterion checking, and primary-diagnosis selection. It records a ranked differential diagnosis, criterion states (\texttt{met}, \texttt{not\_met}, or \texttt{insufficient\_evidence}), a criterion-compatible set, and the final commitment.

Stage-wise analysis showed that the largest recorded disagreement group in both datasets occurred at the primary-diagnosis selection stage: 272 cases in LingxiDiag-16K and 225 cases in MDD-5k. In these cases, at least one gold label was already in the Top-3 and the criterion-compatible set, but the system still selected another primary diagnosis. The tested re-selection methods did not show a clear improvement.

HiED's main contribution is therefore not higher diagnostic accuracy, but a structured record that is designed to support faster clinical review by helping clinicians screen candidate diagnoses, locate the symptoms and criterion evidence relevant to each candidate, and identify what information still needs to be collected. HiED is a decision-support research framework, not an autonomous diagnostic system. The evaluation uses synthetic Chinese transcripts; real-patient evaluation is outside the scope of this thesis.

\noindent\textbf{Keywords:} Large language models, multi-agent systems, psychiatric differential diagnosis, clinical decision support, ICD-10, auditable AI
"""

OLD_INTRO_SENTENCE = (
    "These outputs are designed to help clinicians review the case, narrow the candidate list, "
    "and decide what should be checked next."
)
NEW_INTRO_SENTENCE = (
    "These outputs are designed to support faster clinical review by helping clinicians screen "
    "candidate diagnoses, locate the symptoms and criterion evidence relevant to each candidate, "
    "and identify what information still needs to be collected."
)


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise SystemExit(f"Expected unique markers: {start_marker!r}, {end_marker!r}")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement.rstrip() + "\n" + text[end:]


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    original = text
    comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))

    text = replace_between(text, r"\chapter*{中文摘要}", r"\chapter*{Abstract}", CHINESE_ABSTRACT)
    text = replace_between(text, r"\chapter*{Abstract}", r"\chapter*{Acknowledgements}", ENGLISH_ABSTRACT)

    if text.count(OLD_INTRO_SENTENCE) != 1:
        raise SystemExit(f"Expected one old Introduction sentence, found {text.count(OLD_INTRO_SENTENCE)}")
    text = text.replace(OLD_INTRO_SENTENCE, NEW_INTRO_SENTENCE, 1)

    if comment_counts != (text.count(r"\ct{"), text.count(r"\wl{")):
        raise SystemExit("Advisor-comment counts changed")

    required = [
        "Many psychiatric LLM systems are diagnosis-centered",
        "272 cases in LingxiDiag-16K and 225 cases in MDD-5k",
        "at least one gold label was already in the Top-3",
        "HiED's main contribution is therefore not higher diagnostic accuracy",
        "HiED is a decision-support research framework, not an autonomous diagnostic system",
        "分階段分析顯示，兩個資料集中最多的已記錄分歧都出現在主診斷選擇階段",
        "LingxiDiag-16K 有 272 例，MDD-5k 有 225 例",
        "至少一個資料集標準答案已進入前三個候選",
        "HiED 的主要貢獻不是提高診斷準確率",
        NEW_INTRO_SENTENCE,
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Missing approved content: {missing}")

    abstract_start = text.index(r"\chapter*{Abstract}")
    ack_start = text.index(r"\chapter*{Acknowledgements}", abstract_start)
    english = text[abstract_start:ack_start]
    for stale in ["51.8\\% Top-1", "80.2\\% genuine Top-3", "TF--IDF with logistic regression gave stronger"]:
        if stale in english:
            raise SystemExit(f"Stale accuracy-centered abstract wording remains: {stale}")

    if text == original:
        raise SystemExit("No source change produced")

    TARGET.write_text(text, encoding="utf-8")
    print(f"Updated {TARGET}")
    print(f"Characters: {len(original)} -> {len(text)}")
    print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")


if __name__ == "__main__":
    main()
