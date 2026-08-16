from __future__ import annotations

import sys
from pathlib import Path


def replace_once(source: str, old: str, new: str, label: str) -> str:
    count = source.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return source.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: reframe_psychiatrist_review.py THESIS_TEX")

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "HiED 旨在支援而非取代醫師。量化結果來自合成中文逐字稿；針對部分 LingxiDiag 案例的盲性精神科醫師標注仍待完成，真實病人評估不在本論文範圍內。",
        "HiED 旨在支援而非取代醫師。量化結果來自合成中文逐字稿；針對部分 LingxiDiag 合成案例的單一精神科醫師標籤一致性審查（初始診斷階段採盲性設計）列為後續工作，未納入本論文結果；真實病人評估亦不在本論文範圍內。",
        "Chinese abstract future-work sentence",
    )

    text = replace_once(
        text,
        "A blinded psychiatrist annotation study on selected LingxiDiag cases remains pending, and real-patient evaluation is outside the scope of this thesis.",
        "A proposed single-psychiatrist benchmark-label alignment review with a blinded initial assessment is documented as future work and contributes no clinician-derived result to this thesis; real-patient evaluation is also outside its scope.",
        "English abstract future-work sentence",
    )

    text = replace_once(
        text,
        "Her deep expertise in psychiatric diagnosis and her clinical\nguidance shaped both the differential-diagnosis framework and the\npsychiatrist annotation study for selected LingxiDiag cases.",
        "Her deep expertise in psychiatric diagnosis and her clinical\nguidance shaped both the differential-diagnosis framework and the\nproposed psychiatrist review protocol for selected LingxiDiag cases.",
        "Acknowledgements protocol wording",
    )

    old_ch5_intro = (
        "This chapter separates configuration selection, held-out evaluation, supporting sensitivity analyses, and a pending clinician-review protocol. "
        "These parts use different populations and support different claims. Validation results select configurations; the internal held-out set provides "
        "the main internal estimate; MDD-5k provides the second-synthetic-source stage-wise analysis; and the pending psychiatrist protocol defines a planned "
        "review of a small, selected synthetic disagreement sample."
    )
    new_ch5_intro = (
        "This chapter describes the completed configuration-selection, held-out-evaluation, primary-selection, and supporting boundary analyses. "
        "These analyses use different populations and support different claims. Validation results select configurations; the internal held-out set provides "
        "the main internal estimate; and MDD-5k provides the second-synthetic-source stage-wise analysis. A separate final section documents a proposed "
        "post-thesis psychiatrist review protocol for selected synthetic cases. That protocol was not conducted within the thesis period and is not part of "
        "the completed evidence."
    )
    text = replace_once(text, old_ch5_intro, new_ch5_intro, "Chapter 5 opening")

    old_population_row = r"""\hline
Pending blinded psychiatrist annotation protocol & Twenty cases to be sampled from the 272-case $D_3=1$, $I=1$, $S=0$ group & Pending protocol for a selected synthetic disagreement sample; no clinician results are included in the completed evidence\\
\hline
"""
    text = replace_once(text, old_population_row, "", "Analysis-population future-work row")

    start_marker = r"\section{Blinded Psychiatrist Annotation Protocol (Pending)}"
    end_marker = r"\chapter{Internal Evaluation Results}"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise SystemExit("Psychiatrist protocol markers are not unique")
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    protocol = r"""\section{Proposed Single-Psychiatrist Review of Benchmark-Label Alignment (Future Work)}
\label{sec:clinical-evaluation-plan}
\label{sec:lingxidiag-pilot-review}

The following protocol is documented as future work and was not conducted within the thesis period. It contributes no clinician-derived result to the present thesis. Its purpose is to examine whether the benchmark diagnoses assigned to selected synthetic LingxiDiag transcripts are concordant with one psychiatrist's transcript-only diagnostic assessment. It is not designed to establish dataset-wide label validity, inter-rater reliability, clinical diagnostic accuracy, or clinical validation of HiED.

Twenty cases will be sampled without replacement from the 272-case group satisfying $D_3=1$, $I=1$, and $S=0$. This purposive sample focuses on cases in which a benchmark-reference diagnosis is present in both the genuine Top-3 and the criterion-compatible set but is not committed as primary by HiED. The observations will therefore apply only to this selected disagreement subgroup and will not be interpreted as an estimate for the full LingxiDiag dataset.

One psychiatrist will review the selected transcripts in a randomized order. During the initial diagnostic assessment, the reviewer will remain blinded to the LingxiDiag benchmark labels, HiED ranked and committed diagnoses, Criterion Checker outputs, the $D_3$--$I$--$S$ profile, and the case-selection rationale. The reviewer will not be restricted to HiED's fourteen configured diagnostic categories and may record another diagnosis or indicate that the transcript contains insufficient information.

Before any benchmark label is shown, the psychiatrist will record whether the transcript supports a unique primary diagnosis, only a provisional primary diagnosis, or no sufficiently supported primary diagnosis. The reviewer will then record one primary diagnosis, up to three ranked differential diagnoses, possible comorbid diagnoses, diagnostic confidence, and a brief explanation of the evidence and missing information relevant to the judgment.

After the blinded transcript-only assessment is locked, the benchmark label or labels will be shown only for a second-stage label-appraisal question, while all HiED outputs remain concealed. For each benchmark label, the psychiatrist will classify it as aligned with the primary diagnosis, plausible as a comorbid or differential diagnosis but not primary, not supported by the transcript, or not judgeable because the transcript is insufficient.

Descriptive analyses will report primary-diagnosis concordance, benchmark-label coverage in the ranked differential or comorbidity set, the second-stage plausibility classification, and the frequency of insufficient-information judgments. No inter-rater agreement, consensus adjudication, criterion-state validation, or population-level clinical-accuracy estimate will be reported.

Because the review contains only twenty purposively selected synthetic cases and one psychiatrist, it will be interpreted as a preliminary single-expert benchmark-label audit rather than as independent clinical validation of the dataset or the system.

"""
    text = text[:start] + protocol + text[end:]

    old_limitation = (
        r"The blinded LingxiDiag psychiatrist annotation study described in Section~\ref{sec:clinical-evaluation-plan} is the only clinician-facing study retained in this thesis. "
        r"It uses a purposively selected sample of synthetic disagreement cases. Until completed, it provides no clinician evidence. Even after completion, it can assess how "
        r"psychiatrists interpret the selected synthetic cases, but it cannot estimate clinical accuracy, diagnostic prevalence, workflow benefit, or performance in a representative patient population."
    )
    new_limitation = (
        r"No psychiatrist review was completed within the thesis period, so the present thesis contains no clinician-derived evidence. Section~\ref{sec:clinical-evaluation-plan} "
        r"documents a proposed single-psychiatrist benchmark-label alignment review with a blinded initial assessment as future work. Because the proposed review uses one psychiatrist "
        r"and a purposively selected sample of synthetic disagreement cases, even a completed review would characterize one expert's transcript-only assessment of those cases rather than "
        r"establish dataset-wide label validity, clinical accuracy, diagnostic prevalence, workflow benefit, or performance in a representative patient population."
    )
    text = replace_once(text, old_limitation, new_limitation, "Chapter 10 clinician boundary")

    old_future_intro = (
        "Within the current thesis project, the only retained follow-up study is the blinded LingxiDiag psychiatrist annotation described below. "
        "The other items are broader directions for independent future research and are not part of the completed experimental scope."
    )
    new_future_intro = (
        "The proposed single-psychiatrist LingxiDiag review described below is documented as future work. It was not conducted within the thesis period and contributes no "
        "clinician-derived evidence to the completed thesis. The other items are broader directions for independent future research and are not part of the completed experimental scope."
    )
    text = replace_once(text, old_future_intro, new_future_intro, "Chapter 11 future-work opening")

    fw_start_marker = r"\paragraph{Complete and report the LingxiDiag psychiatrist annotation study.}"
    fw_end_marker = r"\paragraph{Model direct comparisons among candidates.}"
    if text.count(fw_start_marker) != 1 or text.count(fw_end_marker) != 1:
        raise SystemExit("Future-work paragraph markers are not unique")
    fw_start = text.index(fw_start_marker)
    fw_end = text.index(fw_end_marker, fw_start)
    future_paragraph = r"""\paragraph{Conduct a single-psychiatrist review of benchmark-label alignment.}

A proposed follow-up review will examine whether the benchmark diagnoses assigned to twenty selected synthetic disagreement cases are concordant with one psychiatrist's transcript-only diagnostic assessment. The initial assessment will be completed without access to the benchmark labels or HiED outputs. After that assessment is locked, benchmark-label alignment will be summarized as primary agreement, presence in the ranked differential or comorbidity set, plausible-but-not-primary alignment, unsupported labeling, or insufficient transcript evidence. The detailed protocol is documented in Section~\ref{sec:clinical-evaluation-plan}. Because the review uses one psychiatrist and a purposively selected synthetic sample, it will not establish dataset-wide label validity or clinical diagnostic accuracy.

"""
    text = text[:fw_start] + future_paragraph + text[fw_end:]

    old_final = (
        "HiED's completed contribution is a stage-wise and inspectable output contract rather than a clinically validated diagnostic tool. "
        "The retained LingxiDiag annotation study will examine how clinicians interpret selected records; broader clinical validation and deployment remain independent future research."
    )
    new_final = (
        "HiED's completed contribution is a stage-wise and inspectable output contract rather than a clinically validated diagnostic tool. "
        "The proposed single-psychiatrist review may provide a preliminary audit of benchmark-label alignment in selected synthetic disagreement cases, while broader clinical validation "
        "and deployment remain independent future research."
    )
    text = replace_once(text, old_final, new_final, "Final thesis sentence")

    required = [
        "Proposed Single-Psychiatrist Review of Benchmark-Label Alignment (Future Work)",
        "One psychiatrist will review the selected transcripts",
        "No inter-rater agreement, consensus adjudication, criterion-state validation",
        "No psychiatrist review was completed within the thesis period",
        "Conduct a single-psychiatrist review of benchmark-label alignment",
        "contributes no clinician-derived result to this thesis",
    ]
    forbidden = [
        "Blinded Psychiatrist Annotation Protocol (Pending)",
        "Two psychiatrists will independently review all cases",
        "pre-consensus inter-rater agreement",
        "Complete and report the LingxiDiag psychiatrist annotation study",
        "Pending blinded psychiatrist annotation protocol",
        "A blinded psychiatrist annotation study on selected LingxiDiag cases remains pending",
    ]
    for item in required:
        if item not in text:
            raise SystemExit(f"Missing required text: {item}")
    for item in forbidden:
        if item in text:
            raise SystemExit(f"Forbidden legacy text remains: {item}")
    if text.count(r"\label{sec:clinical-evaluation-plan}") != 1:
        raise SystemExit("clinical-evaluation-plan label count is not one")
    if text.count(r"\label{sec:lingxidiag-pilot-review}") != 1:
        raise SystemExit("lingxidiag-pilot-review label count is not one")

    path.write_text(text, encoding="utf-8")
    print(f"updated {path}")


if __name__ == "__main__":
    main()
