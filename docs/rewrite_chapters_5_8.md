# Conference-style rewrite: chapters 5--8

## Chapter 5: HiED System Architecture

Opening replacement:

HiED is designed to expose the structure of diagnostic failure. Its components are not added on the assumption that more modules improve accuracy; they are separated so that candidate generation, criterion verification, deterministic aggregation, and final selection can be varied or inspected independently. This makes the architecture both a decision-support prototype and an experimental instrument for causal attribution.

Algorithmic summary to add:

1. Normalize the transcript while preserving speaker turns.
2. Retrieve class-balanced supporting cases with FAISS/BGE-M3.
3. Prompt the diagnostician to emit a ranked differential, committed primary, optional comorbidity, confidence, and rationale.
4. Run disorder-specific ICD-10 criterion checkers over candidate diagnoses.
5. Convert checker outputs into met, not-met, and insufficient-evidence states.
6. Apply deterministic threshold logic to produce a logic-confirmed set.
7. Emit the primary diagnosis, ranked differential, optional comorbidity, criterion trace, logic results, and decision trace.

Key wording changes:

- The audit trace is output-side evidence, not proof of the model's internal reasoning.
- Direct-Answer and Nominate-then-Select share upstream outputs, so differences isolate finalization.
- Ontology expansion shows representational configurability, not behavioral retargeting.
- Pairwise reasoning is a repair probe, not part of the selected headline architecture.
- Local inference is an infrastructure property, not clinical validity.

Closing transition:

Because HiED separates these functions, the experiments can now ask which stage actually limits performance and whether targeted repairs can close the gap.

## Chapter 6: Experimental Design

Opening replacement:

The experiments convert the selection-bottleneck hypothesis into a controlled test battery. Each variant is included because it corresponds to a specific alternative explanation: perhaps the system lacks retrieval, perhaps verification should re-select the primary, perhaps local comparison is needed, perhaps debate or sampling reveals hidden consensus, or perhaps a simple deterministic fusion rule is missing. A negative result is interpretable only because the intervention is tied to the mechanism it tests.

Negative-result framing:

The repair battery does not merely record failed attempts. It narrows the explanation space. If a global threshold, simple fusion rule, additional reasoning round, pairwise override, or sampling majority were sufficient, at least one controlled probe should move committed Top-1 under the frozen protocol. Their convergence around no stable causal gain supports the interpretation that the residual error lies in comparative primary selection under incomplete transcript evidence.

Closing transition:

The next chapter applies this design to the in-domain internal test split, first measuring whether the correct diagnosis is present, then asking why it is not selected.

## Chapter 7: In-Domain Results

Opening replacement:

The in-domain results show that HiED's measured strength and weakness occur at different stages. Retrieval improves direct classification and HiED provides a ranked differential and audit trace, but the largest gap is between coverage and commitment: the correct diagnosis is often available to the system before the final primary is chosen.

Result interpretation rewrites:

- Retrieval improves candidate support, but it does not explain the remaining Top-3/Top-1 gap.
- Verification retains the gold diagnosis, but its low selectivity prevents it from choosing the primary.
- NtS improves set control while lowering Top-1, so it is not a primary-selection improvement.
- Checker factorial flatness rules out checker granularity or global thresholds as sufficient explanations.
- Pairwise reasoning, debate, fusion, self-consistency, and confidence-weighted aggregation fail for different reasons but converge on the same conclusion: the system lacks a transferable comparative selector.
- Size robustness shows reduced sensitivity across backbones, not proof that capacity is irrelevant.
- Confusion around depression, anxiety, and mood boundaries is consistent with missing temporal and exclusion evidence.

Closing transition:

The internal results localize the failure to primary selection among already plausible and often verified candidates. The next chapter tests whether this localization survives distribution shift and scope expansion.

## Chapter 8: External Synthetic Evaluation and Scope Transfer

Recommended title:

External Synthetic Evaluation and Configuration-Level Scope Transfer

Opening replacement:

The external evaluation asks whether the in-domain failure decomposition is corpus-specific or structurally persistent. MDD-5k provides a different synthetic distribution and a broader label space, so it is useful for distribution-shift evidence but not for clinical validation. The chapter therefore separates in-scope transfer, out-of-scope coverage, mechanical ontology expansion, lexical transfer, and external repair behavior.

Interpretation rewrite:

Coarse F32/F41 discrimination transfers, but full multi-way primary selection remains difficult. Out-of-scope cases are coverage limits rather than recoverable selector errors. Mechanical expansion makes additional codes representable but does not make them recoverable as primaries. Lexical and case-similarity rerankers fit in-domain regularities but fail or degrade under distribution shift. The external repair battery therefore preserves the in-domain conclusion: no tested repair supplies a stable transferable selector.

Closing transition:

The external results show that the bottleneck is not merely an in-domain artifact. The next chapter translates the aggregate pattern into error archetypes that reveal how the failure appears at the case level.
