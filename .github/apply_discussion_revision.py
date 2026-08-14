from __future__ import annotations

import sys
from pathlib import Path


DISCUSSION = r"""\chapter{Discussion}
\label{ch:discussion}

The results support a stage-wise interpretation of HiED rather than an accuracy-leading claim. TF--IDF with logistic regression provides the strongest same-source primary-label and class-level F1 performance in the main internal comparison, while Single and HiED have almost the same committed Top-1 result. HiED's distinct contribution is therefore not higher final-label accuracy, but the set of recorded outputs that makes candidate generation, criterion checking, compatibility analysis, and primary commitment separately observable.

The internal and external analyses show the same broad type of benchmark disagreement: a reference diagnosis can remain present in both the ranked candidates and the criterion-compatible set while another diagnosis is committed as primary. The frequency of this profile differs across datasets and archived traces. The stage-wise questions therefore transfer more clearly than the numerical rates themselves.

\section{Interpreting Compatibility and Primary Commitment}
\label{sec:discussion-primary-selection}

Candidate generation, criterion checking, and primary commitment answer different questions. Candidate generation identifies diagnoses that remain plausible. Criterion checking asks whether the fixed transcript supports each configured diagnosis under the study rules. Primary commitment asks which diagnosis should be selected after the plausible alternatives are compared.

Several psychiatric diagnoses can be compatible with the same incomplete transcript. Shared findings such as poor sleep, fatigue, poor concentration, low mood, worry, avoidance, and impaired daily function may support more than one category. A diagnosis that passes its own compatibility rule may therefore be the primary diagnosis, a comorbid condition, a secondary explanation, a less specific alternative, or a diagnosis that still requires more information.

This distinction is reflected in the recorded outputs. The internal criterion-compatible set contains a median of six configured categories, and its size and aggregate criterion-state composition do not clearly separate committed-primary agreement from the largest primary-commitment disagreement group. The external results likewise show that compatibility is neither sufficient for a diagnosis to be committed as primary nor necessary for Direct-Answer to retain a benchmark-consistent primary.

The 272 internal cases and 225 external cases in which a reference diagnosis is ranked and compatible but no benchmark-reference parent is committed as primary are therefore best interpreted as recorded primary-commitment disagreements. They show that candidate availability and criterion compatibility do not uniquely determine the final commitment. They do not prove that the finalizer alone caused the disagreement, that the benchmark diagnosis is the uniquely correct clinical primary, or that primary selection is the largest clinical difficulty in other settings.

The results suggest that future selectors may need comparative evidence that is not represented by independent compatibility checks alone. Such evidence may include symptom timing, illness course, episode structure, syndrome dominance, exclusionary causes, explanatory dependence, and the relation between primary and comorbid diagnoses. This is a design hypothesis motivated by the observed results, not a demonstrated solution.

\section{Relation to Existing Psychiatric LLM and Decision-Support Systems}
\label{sec:discussion-related-systems}

HiED is not the first psychiatric system to use multiple agents, diagnostic criteria, structured states, or intermediate reasoning records. Interactive systems such as MIND, WiseMind/ProAI, MAGI, and DSM5AgentFlow use criteria-guided or multi-stage workflows and can collect additional information during an assessment~\citep{li2026mind,wu2026wisemind,bi2025magi,ozgun2025dsm5agentflow}. Fixed-record systems such as MentalSeek-Dx and MoodAngels also organize diagnostic reasoning around symptoms or diagnostic criteria~\citep{sun2026mentalseek,xiao2025moodangels}.

The narrower contribution of HiED is the evaluation contract used in this thesis. Ranked candidates, criterion states, the criterion-compatible set, and the committed primary diagnosis are retained for the same cases and evaluated as separate output views. This makes it possible to distinguish candidate absence, compatibility disagreement, and primary-commitment disagreement without claiming access to hidden model reasoning. The contribution is therefore stage-wise observability and disagreement localization, not the first use of agents or diagnostic criteria.

Structured-knowledge and rule-based systems provide another useful comparison. MedKGI and DKEC show how external knowledge structures can support evidence collection or multilabel prediction, while constraint-logic decision support emphasizes inspectable diagnostic rules~\citep{wang2025medkgi,ge2024dkec,kim2025clp}. The present results show an additional boundary: satisfying an individual compatibility rule does not by itself rank several compatible psychiatric diagnoses or identify which one should be primary. Criterion records should therefore be treated as structured evidence for comparison and review, rather than as an automatic primary-diagnosis ordering.

\section{Why Additional Selection Inference Did Not Close the Gap}
\label{sec:discussion-selection-strategies}

DA versus NtS provides the most controlled primary-selection comparison because both policies reuse the same ranked candidates, criterion states, and criterion-compatible set. NtS lowers committed Top-1 under all three internal retrieval settings. One plausible explanation is that several diagnoses pass broad compatibility rules, leaving a compatibility-first rule with insufficient information to decide which diagnosis should be primary. Such a rule can correct some disagreements but can also replace an initially benchmark-consistent DA choice.

Deterministic fusion applies another fixed summary of the same records and also does not provide a clear gain. Pairwise comparison, debate, and repeated generation make candidate comparison more explicit, but they also change prompts, model calls, context arrangements, decoding, or sampling budgets. Their results must therefore be interpreted as comparisons of complete configurations rather than isolated tests of one finalization component.

The fixed-input setting is important for interpreting these negative results. All tested methods receive the same transcript and cannot ask follow-up questions. Additional inference can reorganize the recorded evidence, but it cannot establish facts that the transcript does not contain, such as symptom onset, previous episodes, exclusionary medical causes, or the temporal relation between anxiety and mood symptoms. Interactive psychiatric systems address a different setting because they can seek new evidence during the assessment~\citep{li2026mind,wu2026wisemind,bi2025magi,ozgun2025dsm5agentflow}.

The experiments therefore do not show that additional reasoning or every future selector must fail. They show that the tested rules, prompts, and inference budgets did not reliably convert candidate availability into better committed-primary agreement when operating on the same fixed and possibly incomplete transcript. The Top-3--Top-1 difference is decision headroom, not demonstrated automatic recoverability.

\section{Implications and Boundaries for Auditable Decision Support}
\label{sec:discussion-set-scope-transfer}
\label{sec:discussion-clinical-implications}

Primary commitment is only one part of the diagnostic output. Diagnostic-set construction determines which additional diagnoses are emitted, and 109 cases retain benchmark-consistent primary commitment while differing from the complete benchmark diagnosis set. Diagnostic scope is another boundary because a diagnosis that is absent from the configured output space cannot be ranked, checked, or emitted. Source dependence is a third boundary: the TF--IDF baseline is strong under same-source evaluation but shows limited and asymmetric transfer between the two tested synthetic corpora.

These results identify several separate problems---candidate absence, broad or trace-sensitive compatibility, primary commitment, complete-set construction, diagnostic scope, and source-specific prediction. They should not all be described as one finalization problem, because they require different evidence and different interventions.

HiED preserves a ranked differential, criterion states, short evidence notes, a criterion-compatible set, and the finalization source. A reviewer can inspect whether a diagnosis was absent from the ranking, absent from the compatible set, or present in both views but not committed as primary. This is more informative than a final label alone.

However, inspectability is not correctness or full interpretability. The saved criterion states and evidence notes are model-generated, may contain unsupported evidence or incorrect states, and do not reveal the model's hidden reasoning. Auditability in this thesis means that observable outputs are retained for review and analysis; it does not mean that the system has been clinically validated.

The recorded insufficient-evidence states also suggest a possible direction for future decision support. Rather than repeatedly selecting from the same incomplete record, a system could state which distinction remains unresolved, propose a focused follow-up question, or return an explicit insufficient-information, abstention, or referral result. These behaviors were not evaluated in this thesis and remain design implications rather than demonstrated clinical benefits.

Overall, HiED demonstrates how several diagnostic output views can be made visible under synthetic benchmark conditions. Its clinical usefulness, safety, and workflow effects still require independent clinician adjudication, natural clinical data, prospective evaluation, privacy and governance controls, and continued monitoring.
"""


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: apply_discussion_revision.py TARGET_TEX")

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    start_marker = "\\chapter{Discussion}\n\\label{ch:discussion}"
    end_marker = "\\chapter{Limitations and Threats to Validity}"

    if text.count(start_marker) != 1:
        raise RuntimeError(
            f"expected one Discussion chapter marker, found {text.count(start_marker)}"
        )
    if text.count(end_marker) != 1:
        raise RuntimeError(
            f"expected one Limitations chapter marker, found {text.count(end_marker)}"
        )

    start = text.index(start_marker)
    end = text.index(end_marker, start)
    revised = text[:start] + DISCUSSION.rstrip() + "\n\n" + text[end:]

    discussion_block = revised[start : revised.index(end_marker, start)]
    required = (
        "\\section{Interpreting Compatibility and Primary Commitment}",
        "\\section{Relation to Existing Psychiatric LLM and Decision-Support Systems}",
        "\\section{Why Additional Selection Inference Did Not Close the Gap}",
        "\\section{Implications and Boundaries for Auditable Decision Support}",
        "\\label{sec:discussion-primary-selection}",
        "\\label{sec:discussion-related-systems}",
        "\\label{sec:discussion-selection-strategies}",
        "\\label{sec:discussion-set-scope-transfer}",
        "\\label{sec:discussion-clinical-implications}",
        "stage-wise observability and disagreement localization",
        "fixed and possibly incomplete transcript",
        "design implications rather than demonstrated clinical benefits",
    )
    missing = [item for item in required if item not in discussion_block]
    if missing:
        raise RuntimeError(f"revised Discussion is missing required content: {missing}")

    forbidden = (
        "A stronger primary selector would need direct comparisons among candidates.",
        "This is expected when several diagnoses pass broad compatibility rules.",
        "An earlier F60 scope-expansion result could not be linked",
        "\\section{Compatibility and Primary Selection in the Evaluated Trace}",
        "\\section{Boundaries Beyond Primary Selection}",
    )
    remaining = [item for item in forbidden if item in discussion_block]
    if remaining:
        raise RuntimeError(f"obsolete Discussion content remains: {remaining}")

    path.write_text(revised, encoding="utf-8")
    print(f"Applied Discussion revision to {path}")


if __name__ == "__main__":
    main()
