# Conference-style rewrite: chapters 9--13

## Chapter 9: Error Archetypes and Worked Analyses

Opening replacement:

Aggregate metrics identify where the system fails, but error archetypes show how the failure becomes visible in individual cases. The examples in this chapter map each error to a stage of the decomposition: scope, candidate detection, criterion retention, confirmed-set size, missing evidence, finalization, and cross-corpus stability.

Add this compact archetype table:

| Archetype | Stage exposed | Quantitative evidence it explains | Main implication |
|---|---|---|---|
| Depression--anxiety boundary | Selection | F41/F32 and mood-boundary confusions | Need comparative evidence about duration, onset, and primacy |
| Missing exclusion information | Evidence / verification | High insufficient-evidence burden | Need evidence acquisition, not stricter thresholds alone |
| Correct candidate, wrong commitment | Selection | Top-3 and logic retention exceed Top-1 | Candidate generation is not the limiting stage |
| Conservative set control | Metric trade-off | NtS raises Exact Match but lowers Top-1 | Primary and set metrics must be interpreted separately |
| Out-of-scope diagnosis | Scope | External out-of-scope cases and failed expanded-scope recovery | Representable does not mean recoverable |
| Rare-class failure | Distribution | Low macro-F1 despite moderate weighted metrics | Aggregate accuracy can hide rare-label weakness |

Closing transition:

The archetypes make the bottleneck concrete: the system often has enough evidence to keep the right diagnosis in view, but not enough comparative structure to commit it safely. The discussion now interprets what this means for method design, modality limits, and clinical claims.

## Chapter 10: Discussion

Opening replacement:

The main lesson of HiED is not that a hybrid multi-agent system achieves autonomous psychiatric diagnosis. It is that transcript-only psychiatric diagnosis can be decomposed into stages whose failures differ. HiED detects and verifies plausible diagnoses more often than it selects the correct primary, and this mismatch persists across repair probes and external synthetic shift.

Synthesis replacement:

Verification fails to select because compatibility is not primacy. A criterion checker can establish that several disorders are supported by the same transcript, especially when overlapping symptoms are present and temporal or exclusion evidence is missing. The final decision requires a comparative judgment among supported alternatives, which neither scalar thresholding nor additional generic reasoning supplies under the tested conditions.

Negative-result interpretation:

The negative results constrain the solution space. They do not prove that logic selection, pairwise reasoning, debate, fusion, self-consistency, or learned reranking are useless in general. They show that reasonable implementations of these mechanisms did not close this specific gap under a frozen transcript-only protocol. Future methods must either add comparative structure to selection or acquire the missing evidence that the transcript lacks.

Closing transition:

This interpretation remains bounded by the data, metrics, and clinical setting. The next chapter states those limitations explicitly so that the contribution is read as auditable failure localization rather than clinical validation.

## Chapter 11: Limitations and Threats to Validity

Opening replacement:

The limitations define the evidentiary boundary of the thesis. The experiments support a claim about decomposed failure localization on synthetic transcript corpora; they do not establish Taiwanese clinical effectiveness, clinician-level performance, or autonomous diagnostic safety. Stating these boundaries is necessary because the system's domain is clinical and the temptation to overread benchmark performance is high.

Key wording:

- Synthetic data qualifies every quantitative result.
- Public release means pretraining overlap cannot be excluded.
- The internal carve is not the same as an official public test evaluation.
- Checker states are auditable outputs, not clinician-validated criterion gold.
- Top-3 measures coverage, not correctness.
- Out-of-scope labels cannot be recovered by selection.
- External MDD is distribution shift, not real-patient validation.
- Local inference reduces exposure but does not establish compliance or clinical safety.

Closing transition:

Within these limits, the system can still inform clinical decision-support design. The next chapter describes how a clinician-facing version would need to be governed, monitored, and validated before any real deployment claim could be made.

## Chapter 12: Clinical Deployment, Governance, and Human--AI Collaboration

Opening replacement:

The evaluation supports HiED as clinician-facing decision support, not as an autonomous diagnostic system. The system is best understood as a tool for organizing a differential, exposing criterion evidence, flagging missing information, and supporting clinician review. This intended use follows from the empirical results: HiED is stronger at candidate generation and audit presentation than at unaided primary selection.

Key wording:

- Human oversight is required by the measured selection bottleneck, not added as a generic disclaimer.
- Uncertainty should remain multi-dimensional: low confidence, high insufficient-evidence burden, out-of-scope status, and runtime failure require different responses.
- Local inference is one privacy control, not a complete governance solution.
- Fairness in Taiwanese populations remains unproven until stratified local data are evaluated.
- Treating-clinician comparison and transcript-only blinded expert ceilings answer different validation questions.
- Regulatory classification, safety, and effectiveness remain outside the thesis.

Closing transition:

The deployment analysis reinforces the same boundary as the experiments: the present work provides an auditable research architecture and evidence of a selection bottleneck. The conclusion now states the resulting contribution and the studies it motivates.

## Chapter 13: Conclusions and Future Work

Opening replacement:

This thesis introduced HiED to study a specific failure mode in transcript-only psychiatric LLM diagnosis. By separating candidate detection, criterion verification, and committed primary selection, the system shows that the correct diagnosis can be present and criterion-supported while still not being selected as the primary.

Future-work rewrite:

The next research step is not simply a larger model or another round of debate. The thesis motivates three specific directions: a transcript-only human ceiling to distinguish method limits from information limits; structured selectors over symptoms, criteria, exclusions, and temporal relations; and evidence-acquisition policies that ask for the missing discriminator instead of forcing a primary commitment from incomplete evidence.

Final conclusion replacement:

HiED's contribution is an auditable architecture and a reproducible demonstration that psychiatric LLM diagnosis can fail after the correct diagnosis has already been detected and criterion-supported. Under the tested transcript-only setting, the dominant measured bottleneck is comparative primary selection. The work therefore identifies what future systems must improve and what future evaluations must measure, while stopping short of claiming clinically validated autonomous diagnosis.
