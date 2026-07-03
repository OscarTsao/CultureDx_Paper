# Conference-style rewrite: chapters 1--4

Core spine: HiED is not presented merely as a multi-agent system. It is presented as an auditable experimental instrument for showing that candidate detection, criterion verification, and primary selection can diverge.

## Chapter 1: Introduction

Opening replacement:

Psychiatric diagnosis from a single consultation transcript is a comparative decision under incomplete evidence. Symptoms that support depression, anxiety, stress-related, obsessive-compulsive, somatic, and sleep disorders frequently overlap, while the duration, course, exclusion, and longitudinal evidence needed to separate them may not be elicited. A model that names a plausible diagnosis has therefore not necessarily solved the task: it may detect the correct disorder, and even verify that disorder against diagnostic criteria, while still committing the wrong primary diagnosis.

This thesis studies that gap. HiED decomposes transcript-only diagnosis into candidate detection, ICD-10 criterion verification, and committed primary selection. The central claim is that these functions can diverge, and that measuring them separately reveals a selection bottleneck hidden by ordinary Top-1 reporting.

Contribution rewrite:

1. HiED combines a local LLM diagnostician, class-balanced retrieval, disorder-specific criterion checkers, and deterministic threshold logic.
2. The thesis defines a detection--verification--selection decomposition and measures each stage on the same cases.
3. The experimental battery tests whether retrieval, verification, pairwise comparison, debate, fusion, learned selection, or sampling aggregation can close the selection gap.

Closing transition:

With the research problem defined as a decomposition rather than a single accuracy number, the next chapter establishes the clinical and technical concepts needed to make detection, verification, selection, and auditability precise.

## Chapter 2: Background

Opening replacement:

The architecture in this thesis follows from the structure of the task. Criteria describe symptoms, duration, impairment, course, and exclusions, but transcripts rarely present these requirements as complete checklists. A computational system must therefore preserve three distinctions that ordinary classification collapses: support versus contradiction, absence of evidence versus evidence of absence, and diagnostic compatibility versus diagnostic primacy.

Use this chapter to show why HiED needs separated roles. Retrieval is for candidate breadth, criterion checks are for auditability, deterministic logic is for reproducibility, and final selection is the measured bottleneck rather than an assumed consequence of verification.

Closing transition:

These concepts motivate an architecture that can expose, rather than hide, where the pipeline succeeds and fails. The next chapter positions HiED against related work in psychiatric LLMs, multi-agent reasoning, interpretability, and structured diagnosis.

## Chapter 3: Related Work

Opening replacement:

Prior work has shown that LLMs can answer psychiatric diagnostic questions, simulate clinical dialogue, support criterion-grounded reasoning, and coordinate multiple agents. The gap addressed here is narrower and more diagnostic: existing systems rarely separate whether the correct diagnosis was generated, whether it survived criterion verification, and whether it was finally selected as the primary. HiED targets this missing measurement.

Research gap replacement:

The literature establishes that LLMs can diagnose, consult, explain, and integrate clinical knowledge. What remains under-specified is the relationship among candidate coverage, criterion verification, and primary selection on the same cases. This thesis fills that gap by measuring those stages separately and by testing interventions that each correspond to a specific hypothesized cause of the gap.

Closing transition:

Having identified the missing measurement, the next chapter defines the evaluation contract: datasets, label projection, metrics, split discipline, statistics, and reproducibility lineage.

## Chapter 4: Data and Evaluation Protocol

Opening replacement:

The selection-bottleneck claim is only meaningful if every number refers to a fixed label space, split, metric, and system policy. This chapter therefore defines the evaluation contract before any results are interpreted. It specifies the diagnostic output, projects raw labels into a common parent taxonomy, separates development from the pre-registered internal test split, and records the statistical and run-health checks that make paired comparisons interpretable.

Style direction:

Top-1 should be described as commitment. Top-3 should be described as recoverable coverage. Exact Match should be described as set calibration. MDD-5k should be described as external synthetic distribution shift, not real clinical validation.

Closing transition:

With the evaluation contract fixed, the next chapter introduces the architecture whose stages are designed to make detection, verification, and selection separately observable.
