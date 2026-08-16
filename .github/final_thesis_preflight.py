from __future__ import annotations

import re
import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def patch_thesis(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    replacements = [
        (
            r"\newif\ifshowcomments \showcommentstrue",
            r"\newif\ifshowcomments \showcommentsfalse",
            "disable visible review comments",
        ),
        (
            "Psychiatric outpatient care is easy to access in Taiwan, but large hospitals also face a heavy workload.",
            "Taiwan's National Health Insurance system allows patients to access specialists and higher-tier medical facilities directly, while large medical centers can face high outpatient volumes.",
            "tighten Taiwan outpatient claim",
        ),
        (
            "First, it presents a two-path and stage-wise architecture for psychiatric decision support.",
            "First, this thesis defines a same-case stage-wise output and evaluation contract, implemented through a two-path architecture for psychiatric decision support.",
            "align introduction contribution",
        ),
        (
            "This chapter separates configuration selection, held-out evaluation, supporting sensitivity analyses, and clinician review. These parts use different populations and support different claims. Validation results select configurations; the internal held-out set provides the main internal estimate; MDD-5k tests synthetic cross-corpus transfer; and the psychiatrist study examines a small, selected synthetic disagreement sample.",
            "This chapter separates configuration selection, held-out evaluation, supporting sensitivity analyses, and a pending clinician-review protocol. These parts use different populations and support different claims. Validation results select configurations; the internal held-out set provides the main internal estimate; MDD-5k provides the second-synthetic-source stage-wise analysis; and the pending psychiatrist protocol defines a planned review of a small, selected synthetic disagreement sample.",
            "clarify experimental chapter scope",
        ),
        (
            r"Sensitivity, scope, and transfer analyses (RQ5) & Internal $N=1000$; MDD-5k all cases $N=925$, in-scope cases $N=878$, and F32--F41 subset $N=490$ & Examines model scale and synthetic distribution shift; does not establish real-patient validity\\",
            r"External stage-wise portability (RQ5) and supporting boundary analyses & Internal $N=1000$; MDD-5k all cases $N=925$, in-scope cases $N=878$, and F32--F41 subset $N=490$ & RQ5 applies the same output views to MDD-5k; model scale, lexical transfer, and descriptive disagreement analyses provide supporting boundary evidence and do not establish real-patient validity\\",
            "clarify RQ5 population row",
        ),
        (
            r"Blinded psychiatrist annotation pilot & Twenty cases sampled from the 272-case $D_3=1$, $I=1$, $S=0$ group & Feasibility and exploratory agreement study on a selected synthetic sample; not a population-level clinical-accuracy estimate\\",
            r"Pending blinded psychiatrist annotation protocol & Twenty cases to be sampled from the 272-case $D_3=1$, $I=1$, $S=0$ group & Pending protocol for a selected synthetic disagreement sample; no clinician results are included in the completed evidence\\",
            "mark clinician protocol pending in population table",
        ),
        (
            r"\section{Sensitivity, Scope, and Transfer Analyses}",
            r"\section{External Portability and Supporting Boundary Analyses}",
            "rename RQ5 design section",
        ),
        (
            "RQ5 examines how the observed patterns change with model scale, synthetic corpus, configured diagnostic scope, and lexical transfer.",
            "RQ5 asks whether the same stage-wise output views remain applicable under a second synthetic source. The MDD-5k stage-wise analysis directly answers this question. Model-scale sensitivity, lexical transfer, and descriptive disagreement analyses are reported as supporting boundary analyses rather than as separate components of RQ5.",
            "narrow RQ5 definition",
        ),
        (
            r"\paragraph{Diagnostic-scope expansion.}
A configuration-level experiment expands the profile from 14 to 33 configured categories by adding category-specific checker definitions without changing model weights. This supporting analysis tests whether newly representable benchmark diagnoses enter the ranked candidates or become the committed primary diagnosis. It is evaluated separately from the primary 14-category external analysis.",
            r"\paragraph{Diagnostic-scope boundary.}
An earlier exploratory configuration expanded the profile from 14 to 33 configured categories by adding category-specific checker definitions without changing model weights. Because the corresponding source artifact was not preserved with sufficient provenance, this experiment is excluded from the supported quantitative analyses. The retained methodological boundary is that a diagnosis absent from the configured output space cannot be ranked, checked, or emitted; expanding the scope alone does not establish accurate selection.",
            "remove unsupported scope-expansion experiment claim",
        ),
        (
            "The model-scale and MDD-5k analyses provide the main evidence for RQ5. Scope expansion, lexical transfer, and confusion-pattern analyses provide supporting evidence about the boundaries of the evaluated synthetic setting.",
            "The MDD-5k stage-wise analysis provides the direct evidence for RQ5. Model-scale, lexical-transfer, and confusion-pattern analyses provide supporting evidence about the boundaries of the evaluated synthetic setting. The earlier scope-expansion run is excluded from quantitative claims because its source artifact was not preserved with sufficient provenance.",
            "clarify direct and supporting RQ5 evidence",
        ),
        (
            r"\section{Blinded Psychiatrist Annotation Pilot}",
            r"\section{Blinded Psychiatrist Annotation Protocol (Pending)}",
            "rename pending clinician protocol",
        ),
        (
            "The blinded annotation of 20 selected LingxiDiag cases is the only clinician-facing evaluation included in this thesis. It examines the feasibility of the review procedure and provides psychiatrist characterization of one selected synthetic disagreement population.",
            "The planned blinded annotation of 20 selected LingxiDiag cases is the only clinician-facing study protocol retained in this thesis. Case annotation and analysis remain pending. The protocol is designed to examine the feasibility of the review procedure and to characterize psychiatrist interpretation of one selected synthetic disagreement population.",
            "state clinician study remains pending",
        ),
        (
            "Twenty cases are sampled without replacement from the 272-case group satisfying $D_3=1$, $I=1$, and $S=0$. The random seed and case identifiers are fixed before review. Two psychiatrists independently review all cases in separately randomized orders. They remain blinded to the benchmark labels, HiED outputs, computational disagreement profile, case-selection rationale, and the other reviewer's responses.",
            "Twenty cases will be sampled without replacement from the 272-case group satisfying $D_3=1$, $I=1$, and $S=0$. The random seed and case identifiers will be fixed before review. Two psychiatrists will independently review all cases in separately randomized orders. They will remain blinded to the benchmark labels, HiED outputs, computational disagreement profile, case-selection rationale, and the other reviewer's responses.",
            "use future tense for pending clinician protocol",
        ),
        (
            "This chapter reports the internal results in the order needed to interpret the study. Retrieval configurations are selected first on the public-validation split (RQ3). The frozen configurations are then compared on the fixed internal held-out set (RQ1). The remaining sections localize disagreement across the recorded output views (RQ2), evaluate primary-selection interventions (RQ4), and report the internal model-scale and diagnostic-confusion analyses that contribute to RQ5. All results in this chapter measure agreement with projected benchmark labels on synthetic LingxiDiag dialogues; they are not estimates of clinical diagnostic accuracy.",
            "This chapter reports the internal results in the order needed to interpret the study. Retrieval configurations are selected first on the public-validation split (RQ3). The frozen configurations are then compared on the fixed internal held-out set (RQ1). The remaining sections localize disagreement across the recorded output views (RQ2), evaluate primary-selection interventions (RQ4), and report supporting internal model-scale and diagnostic-confusion analyses. All results in this chapter measure agreement with projected benchmark labels on synthetic LingxiDiag dialogues; they are not estimates of clinical diagnostic accuracy.",
            "remove model scale from direct RQ5 answer",
        ),
        (
            "Both retrieval configurations improve held-out Top-1 over no retrieval, by 5.1 and 4.2 percentage points, respectively.",
            "Both retrieval configurations have higher held-out Top-1 point estimates than no retrieval, by 5.1 and 4.2 percentage points, respectively.",
            "qualify Single retrieval observation",
        ),
        (
            "Retrieval provides a clear Top-1 benefit for the direct Single configuration.",
            "Retrieval produces higher Top-1 point estimates for the direct Single configuration than no retrieval on both the validation and held-out splits.",
            "align RQ3 answer with descriptive evidence",
        ),
        (
            r"\section{Model-Scale and Diagnostic Disagreement Analysis}",
            r"\section{Supporting Model-Scale and Diagnostic Disagreement Analyses}",
            "rename supporting internal analyses",
        ),
        (
            "This section reports the internal model-scale and diagnostic-confusion results that contribute to RQ5. External synthetic transfer, diagnostic-scope expansion, and lexical transfer are reported in Chapter~\\ref{ch:external}.",
            "This section reports supporting internal model-scale and diagnostic-confusion results. These analyses describe internal boundary conditions but do not directly answer RQ5; the second-synthetic-source stage-wise analysis is reported in Chapter~\\ref{ch:external}.",
            "separate internal sensitivity from RQ5",
        ),
        (
            r"\paragraph{Internal contribution to RQ5.}",
            r"\paragraph{Supporting internal boundary findings.}",
            "rename internal RQ5 paragraph",
        ),
        (
            "The internal results give five main answers. Retrieval improves the Single baseline more clearly than HiED,",
            "The internal results give five main answers. Retrieval is associated with larger Top-1 point-estimate differences for Single than for HiED,",
            "qualify Chapter 6 summary",
        ),
        (
            "\\label{tab:external-trace-sensitivity}\n\\label{tab:scope-expansion-results}",
            "\\label{tab:external-trace-sensitivity}",
            "remove stale scope-expansion label",
        ),
        (
            r"\noindent\textit{TF--IDF baseline configuration:} The model is trained on 13,000 source cases. It uses character-boundary 1--2-grams, at most 10,000 features, \texttt{min\_df=2}, \texttt{max\_df=0.95}, and sublinear term frequency. Twelve class-balanced one-vs-rest L-BFGS logistic-regression classifiers use $C=1.0$ and a 2,000-iteration limit. Their probabilities define the ranked labels and thresholded multilabel output.",
            r"\noindent\textit{TF--IDF baseline configuration:} The model is trained on 13,000 source cases. It uses character-boundary 1--2-grams, at most 10,000 features, \texttt{min\_df=2}, \texttt{max\_df=0.95}, and sublinear term frequency. Twelve class-balanced one-vs-rest L-BFGS logistic-regression classifiers use $C=1.0$ and a 2,000-iteration limit. Their probabilities define the ranked labels. The highest-probability class is always emitted as the primary label, and the second-ranked class is additionally emitted when its probability is at least 0.30; no more than two labels are emitted. Ranked Top-3 uses the three highest class scores independently of this emission rule, whereas Exact Match and F1 use the emitted set.",
            "document TF-IDF multilabel emission rule",
        ),
    ]

    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    # Final source-level consistency gates.
    required = [
        r"\showcommentsfalse",
        "same-case stage-wise output and evaluation contract",
        "External Portability and Supporting Boundary Analyses",
        "Blinded Psychiatrist Annotation Protocol (Pending)",
        "Case annotation and analysis remain pending.",
        "Retrieval produces higher Top-1 point estimates",
        "Supporting Model-Scale and Diagnostic Disagreement Analyses",
        "second-ranked class is additionally emitted when its probability is at least 0.30",
    ]
    for needle in required:
        if needle not in text:
            raise RuntimeError(f"missing required thesis text: {needle}")

    forbidden = [
        r"\showcommentstrue",
        "Retrieval provides a clear Top-1 benefit for the direct Single configuration.",
        r"\label{tab:scope-expansion-results}",
        r"\section{Blinded Psychiatrist Annotation Pilot}",
        r"\paragraph{Diagnostic-scope expansion.}",
        r"\paragraph{Internal contribution to RQ5.}",
    ]
    for needle in forbidden:
        if needle in text:
            raise RuntimeError(f"obsolete thesis text remains: {needle}")

    # Fail on duplicate LaTeX labels, which can silently redirect references.
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    duplicates = sorted({label for label in labels if labels.count(label) > 1})
    if duplicates:
        raise RuntimeError(f"duplicate LaTeX labels: {duplicates}")

    path.write_text(text, encoding="utf-8")


def patch_bibliography(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "% Before camera-ready, confirm author given-names expanded from initials (MDD-5k, CPsyCoun,\n% MDAgents) and final venue formatting (ACL Findings / NeurIPS / AAAI).\n",
        "% Thesis bibliography metadata final pass updated in August 2026.\n",
        "replace stale bibliography TODO",
    )
    text = replace_once(
        text,
        "author  = {Ozgun, Mithat Can and Pei, Jiahuan and Hindriks, Koen and Donatelli, Lucia and Liu, Qingzhi and Wang, Junxiao},",
        "author  = {Ozgun, Mithat Can and Pei, Jiahuan and Hindriks, Koen and Donatelli, Lucia and Liu, Qingzhi and Sun, Xin and Wang, Junxiao},",
        "add missing DSM5AgentFlow author",
    )
    text = replace_once(
        text,
        "@article{wang2025medkgi,\n  title   = {{MedKGI}: Iterative Differential Diagnosis with Medical Knowledge Graphs and Information-Guided Inquiring},\n  author  = {Wang, Qipeng and Sheng, Rui and Li, Yafei and Qu, Huamin and Sun, Yushi and Zhu, Min},\n  journal = {arXiv preprint arXiv:2512.24181},\n  year    = {2026}\n}",
        "@article{wang2025medkgi,\n  title   = {{MedKGI}: Iterative Differential Diagnosis with Medical Knowledge Graphs and Information-Guided Inquiring},\n  author  = {Wang, Qipeng and Sheng, Rui and Li, Yafei and Qu, Huamin and Sun, Yushi and Zhu, Min},\n  journal = {arXiv preprint arXiv:2512.24181},\n  year    = {2025}\n}",
        "correct MedKGI year",
    )

    if "Sun, Xin and Wang, Junxiao" not in text:
        raise RuntimeError("DSM5AgentFlow author correction missing")
    if "arXiv preprint arXiv:2512.24181},\n  year    = {2025}" not in text:
        raise RuntimeError("MedKGI year correction missing")
    if "Before camera-ready" in text:
        raise RuntimeError("stale bibliography TODO remains")

    path.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: final_thesis_preflight.py THESIS_TEX REFERENCES_BIB")
    thesis_path = Path(sys.argv[1])
    bib_path = Path(sys.argv[2])
    patch_thesis(thesis_path)
    patch_bibliography(bib_path)
    print(f"patched {thesis_path} and {bib_path}")


if __name__ == "__main__":
    main()
