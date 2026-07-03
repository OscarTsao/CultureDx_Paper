# Page-level conference-style pass

Use this file as the sentence-level rewrite rulebook for `school/main.tex`.

## Core sentence rule

Every paragraph should end by telling the reader what the paragraph proves, rules out, or motivates.

## Replace thesis narration with research implication

| Current thesis-style tendency | Rewrite direction |
|---|---|
| This thesis is careful to distinguish X from Y. | We distinguish X from Y because conflating them would overstate the evidence. |
| This distinction is maintained throughout. | This distinction prevents a coverage result from being misread as clinical correctness. |
| The following chapter introduces... | The next chapter fixes the evaluation contract needed for the bottleneck claim. |
| Several interventions were tested. | Each intervention tests a specific alternative explanation for the selection gap. |
| The result was negative. | The result rules out this mechanism as a sufficient explanation under the tested protocol. |
| This is a limitation. | This limitation defines the boundary of the claim. |
| The system is not clinically validated. | The evidence supports auditable failure localization, not autonomous clinical use. |

## Required recurring terms

Use these terms consistently:

- candidate detection
- criterion verification
- primary selection
- selection bottleneck
- audit trace
- output-side audit
- external synthetic evaluation
- distribution-shift evidence
- clinician-facing decision support
- transcript-only human ceiling

Avoid terms that overclaim:

- clinical validation, unless explicitly qualified
- interpretable model, when the claim is only an audit trace
- autonomous diagnosis
- state of the art, unless benchmark protocols are fully comparable
- Taiwanese validation, because real-patient Taiwanese evidence is not yet included

## Results paragraph template

Use this structure for each results paragraph:

1. State the measured result.
2. State which stage it affects: detection, verification, selection, transfer, set calibration, or auditability.
3. State what explanation it supports or rules out.
4. State the boundary of the claim.

Example:

Retrieval improves the direct baseline, indicating that similar-case context helps candidate support. However, the remaining Top-3/Top-1 gap persists after retrieval, so retrieval cannot explain the residual primary-selection failure. The result therefore supports retrieval as a coverage mechanism, not as a solution to comparative selection.

## Discussion paragraph template

Use this structure:

1. What the evidence showed.
2. Why the simple interpretation is insufficient.
3. What mechanism remains plausible.
4. What future evidence is required.

Example:

Verification retains the correct diagnosis more often than the final system selects it. This does not make verification useless; it shows that compatibility is easier than primacy. The remaining problem is comparative selection among supported alternatives, especially when temporal and exclusion evidence is missing. Distinguishing method failure from information limits requires a transcript-only human reference.

## Abstract and conclusion alignment

The abstract, introduction, discussion, limitations, and conclusion should all repeat the same bounded contribution:

> HiED provides an auditable decomposition of transcript-only psychiatric LLM diagnosis and shows that candidate detection and criterion verification can exceed committed primary selection. It does not establish autonomous clinical diagnosis.

## Final manuscript checklist

- Remove visible mentor comments such as `CT: Redo...` from final builds.
- Replace the English abstract with the 192-word optimized version.
- Replace the Chinese abstract with the Traditional-Chinese optimized version.
- Rename or qualify `External Validation` as `External Synthetic Evaluation`.
- Add an algorithm box or compact algorithmic summary to the architecture chapter.
- Add a compact archetype table to the error-analysis chapter.
- Add artifact IDs or hashes near headline numbers when available.
- Ensure every chapter closes by pointing to the next chapter's role in the argument.
