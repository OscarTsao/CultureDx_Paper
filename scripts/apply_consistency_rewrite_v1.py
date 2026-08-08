from __future__ import annotations

from pathlib import Path
import re
import sys

TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("school/main.tex")
ROOT = Path(__file__).resolve().parent
CH8 = (ROOT / "consistency_v1" / "chapter8.tex").read_text(encoding="utf-8").strip()
ENDMATTER = (ROOT / "consistency_v1" / "endmatter.tex").read_text(encoding="utf-8").strip()

text = TARGET.read_text(encoding="utf-8")
original = text
comment_counts = (text.count(r"\ct{"), text.count(r"\wl{"))


def replace_exact(old: str, new: str, expected: int = 1) -> None:
    global text
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"Expected {expected} occurrence(s) of {old!r}, found {count}")
    text = text.replace(old, new)


# Front matter and Chapter 1 terminology / claim boundaries.
replace_exact("準則驗證路徑則檢查各診斷的準則", "準則核對路徑則檢查各診斷的準則")
replace_exact(
    "本研究的第一項貢獻，是提出一個能分別記錄與分析候選形成、準則核對與主診斷選擇的架構，並透過這個架構找出主診斷選擇是兩個合成資料集中的最大已記錄分歧類型。",
    "本研究的第一項貢獻，是提出一個能分別記錄與分析候選形成、準則核對與主診斷選擇的架構，並透過這個架構發現：在兩個合成資料集中，最大的已記錄基準分歧都出現在參考診斷已可取得、但另一個診斷被選為主診斷的情況。",
)
replace_exact(
    "本論文唯一納入的臨床人員評估，是針對部分 LingxiDiag 案例進行的盲性精神科醫師標注。",
    "本論文唯一保留的臨床人員研究，是針對部分 LingxiDiag 案例進行的盲性精神科醫師標注。",
)
replace_exact("The criterion path checks each configured diagnosis", "The criterion-checking path checks each configured diagnosis")
replace_exact(
    "This architecture shows that primary diagnosis selection is the largest recorded disagreement group in the two tested synthetic datasets.",
    "This architecture shows that the largest recorded benchmark-disagreement profile in both tested synthetic datasets occurs when a reference diagnosis is available but another diagnosis is committed as primary.",
)
replace_exact(
    "The only clinician-facing evaluation included in this thesis is a blinded psychiatrist annotation study on selected LingxiDiag cases; real-patient clinical evaluation is outside the scope of this thesis.",
    "The only clinician-facing study retained in this thesis is a blinded psychiatrist annotation study on selected LingxiDiag cases; real-patient clinical evaluation is outside the scope of this thesis.",
)
replace_exact(
    "Hospital, who served as the clinical principal investigator for this\nresearch.",
    "Hospital, who provided clinical guidance for this\nresearch.",
)
replace_exact("The criterion path checks every configured diagnosis", "The criterion-checking path checks every configured diagnosis")
replace_exact(
    "A clinician can inspect the possible diagnoses, check which criteria are supported or contradicted, and see which information is still missing.",
    "The outputs are intended to let a clinician inspect the possible diagnoses, check which criteria are supported or contradicted, and see which information is still missing.",
)
replace_exact(
    "Using these outputs, this thesis finds that primary diagnosis selection is the largest recorded disagreement group in the two tested synthetic datasets.",
    "Using these outputs, this thesis finds that primary commitment contains the largest recorded benchmark-disagreement profile in the two tested synthetic datasets.",
)
replace_exact(
    "The only clinician-facing evaluation included in this thesis is a blinded psychiatrist annotation study on selected LingxiDiag cases.",
    "The only clinician-facing study retained in this thesis is a blinded psychiatrist annotation study on selected LingxiDiag cases.",
)

# Standardize prose terminology without changing labels.
text = text.replace("Criterion verification", "Criterion checking")
text = text.replace("criterion verification", "criterion checking")
text = text.replace("Criterion-verification", "Criterion-checking")
text = text.replace("criterion-verification", "criterion-checking")
text = text.replace("準則驗證", "準則核對")

# Replace Chapter 8 with the trace-grounded, plain-language version.
ch8_start = text.index(r"\chapter{Characterization of Recorded-Output Disagreements}")
discussion_start = text.index(r"\chapter{Discussion}", ch8_start)
old_ch8 = text[ch8_start:discussion_start]
if r"\ct{" in old_ch8 or r"\wl{" in old_ch8:
    raise SystemExit("Advisor comments found inside Chapter 8; refusing replacement")
text = text[:ch8_start] + CH8 + "\n\n" + text[discussion_start:]

# Replace Discussion, Limitations, Conclusion, RQ answers, and Future Work as one consistent block.
discussion_start = text.index(r"\chapter{Discussion}")
appendix_start = text.index(r"\appendix", discussion_start)
old_endmatter = text[discussion_start:appendix_start]
if r"\ct{" in old_endmatter or r"\wl{" in old_endmatter:
    raise SystemExit("Advisor comments found inside end matter; refusing replacement")
text = text[:discussion_start] + ENDMATTER + "\n\n" + text[appendix_start:]

if comment_counts != (text.count(r"\ct{"), text.count(r"\wl{")):
    raise SystemExit("Advisor-comment counts changed")

# Global label/reference integrity.
labels = re.findall(r"\\label\{([^}]+)\}", text)
refs: list[str] = []
for pattern in [r"\\ref\{([^}]+)\}", r"\\cref\{([^}]+)\}", r"\\Cref\{([^}]+)\}", r"\\pageref\{([^}]+)\}"]:
    refs.extend(re.findall(pattern, text))
missing_refs = sorted(set(refs) - set(labels))
duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
if missing_refs or duplicate_labels:
    raise SystemExit(f"missing references={missing_refs}; duplicate labels={duplicate_labels}")

required = [
    r"\chapter{Characterization of Recorded-Output Disagreements}",
    r"\label{tab:ch8-joint-profiles}",
    r"\label{fig:ch8-reference-rank}",
    r"\label{tab:ch8-selection-pairs}",
    r"\label{tab:ch8-diagnostic-set-errors}",
    r"\label{fig:ch8-criterion-composition}",
    r"\label{tab:audit-trace-examples}",
    r"\chapter{Discussion}",
    r"\chapter{Limitations and Threats to Validity}",
    r"\chapter{Conclusions and Future Work}",
    "Criterion checking makes this problem easier to inspect, but broad compatibility does not solve the final comparison.",
    "272 of 915 checker-eligible cases",
    "225 of 878 checker-eligible cases",
    "The only clinician-facing study retained in this thesis",
    "Real-patient evaluation is outside the completed thesis scope.",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"Missing required consistency anchors: {missing}")

forbidden = [
    "clinical principal investigator for this research",
    "real-patient validation is ongoing",
    "CGMH real-world validation",
    "scope-expansion experiment in Chapter",
    "primary selection is therefore the largest remaining recorded bottleneck",
]
bad = [item for item in forbidden if item in text]
if bad:
    raise SystemExit(f"Forbidden stale wording remains: {bad}")

if text == original:
    raise SystemExit("Rewrite produced no changes")

TARGET.write_text(text, encoding="utf-8")
print(f"Updated {TARGET}")
print(f"Characters: {len(original)} -> {len(text)}")
print(f"Advisor comments preserved: CT={comment_counts[0]}, WL={comment_counts[1]}")
