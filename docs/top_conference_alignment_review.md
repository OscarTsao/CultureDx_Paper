# Top-conference abstract rewrite and chapter alignment review

Repository: `OscarTsao/CultureDx_Paper`  
Source inspected: `school/main.tex`  
Review target: IEEE / ACL / AI-ML conference style, with special attention to the mentor comment on the abstract.

## Abstract diagnosis

The previous English abstract was factually correct, but it read like an expanded thesis summary. It introduced the system components first, then reported results, but it did not foreground the paper's strongest conference-style contribution: a controlled decomposition showing that candidate detection, criterion verification, and committed primary selection diverge. Top AI/ML and ACL abstracts usually make the contribution legible in the first half of the abstract: problem or gap, proposed method, evaluation setting, headline positive result, headline negative or diagnostic finding, and bounded implication. The optimized abstract therefore moves the selection-bottleneck claim to the center and makes the final sentence a claim-boundary sentence rather than a generic future-work sentence.

A replacement LaTeX block is provided in `school/abstract_optimized_replacement.tex`. It should replace the current `\chapter*{Abstract}` block in `school/main.tex`; the mentor-facing `\ct{Redo...}` comment should not appear in a final build.

## Abstract rewrite principles applied

1. **Lead with the scientific problem, not the component list.** The opening sentence now identifies the task difficulty: overlapping symptoms, missing longitudinal evidence, and absent exclusions.
2. **State the contribution as a decomposition.** HiED is presented as a system, but the main contribution is that it separates candidate detection, criterion verification, and primary selection.
3. **Report the protocol and metrics compactly.** The abstract keeps the internal split size, Top-1/Top-3, retrieval gain, McNemar test, verification-retention result, and external MDD-5k transfer result.
4. **Make the negative result useful.** The repair failures are framed as evidence localizing the bottleneck, not merely as failed attempts.
5. **Preserve clinical claim boundaries.** The revised abstract explicitly says the work is an auditable research architecture, not clinically validated autonomous diagnosis.

## Chapter-by-chapter alignment review

### Front matter and abstract

**Current alignment:** The title and keywords are aligned with AI/ML and clinical decision-support framing. The current abstract contains the necessary facts, but it is too close to a system summary and does not put the detection--verification--selection contribution early enough.

**Required action:** Replace the English abstract with `school/abstract_optimized_replacement.tex`. After the English version is accepted, harmonize the Chinese abstract so it follows the same narrative order and does not imply stronger clinical validation than the English abstract.

### Chapter 1: Introduction

**Current alignment:** Strong. The chapter begins with clinical motivation, explains why transcript-only psychiatric diagnosis is hard, separates candidate detection, criterion verification, and primary selection, and states research questions clearly. This is close to the structure expected in ACL/AI-ML papers: problem, gap, task decomposition, and contributions.

**Suggested refinement:** The contribution list should be kept concise. The best conference-style version would highlight three contributions only: auditable architecture, detection--verification--selection decomposition, and negative repair battery/external transfer.

### Chapter 2: Clinical and Technical Background

**Current alignment:** Strong but slightly long. The chapter defines diagnostic uncertainty, ICD-10 operationalization, auditability, RAG, multi-agent systems, and the formal selection-bottleneck notation.

**Suggested refinement:** Move quickly from general background to the exact research gap. Conference readers will tolerate limited clinical background, but they will expect every paragraph to support the experimental claim. Keep the formal bottleneck definition because it is central and reusable.

### Chapter 3: Related Work

**Current alignment:** Good. The related work covers Chinese psychiatric dialogue resources, psychiatric LLM diagnosis, medical multi-agent reasoning, diagnostic-chain interpretability, synthetic data, knowledge graphs, and the explicit gap. It aligns well with ACL style because it positions the work by mechanism rather than merely listing papers.

**Suggested refinement:** Keep claims about public benchmark comparisons clearly separated from the thesis headline result. When saying HiED exceeds reported frontier/classical baselines on a public validation comparison, preserve all caveats about protocol, label space, and non-headline status.

### Chapter 4: Data and Evaluation Protocol

**Current alignment:** Very strong. The chapter defines the task, split roles, label projection, metrics, statistical tests, run-health gates, leakage control, and reproducibility lineage. This is one of the strongest sections for IEEE/AI-ML review because it addresses leakage, paired statistics, and metric ambiguity.

**Suggested refinement:** Add artifact identifiers or hashes where possible. Reviewers will like the lineage discipline, but they will trust it more if every headline number can be traced to a frozen artifact name.

### Chapter 5: HiED System Architecture

**Current alignment:** Strong. The chapter distinguishes the diagnostician, retrieval, criterion checkers, deterministic logic, finalization policies, output/audit trace, ontology scope, pairwise reasoning, and computational configuration. It correctly avoids claiming that the audit trace is faithful model reasoning.

**Suggested refinement:** Add an algorithm box or pseudo-code block if page limits permit. AI/ML reviewers often expect a compact procedural statement of the pipeline in addition to prose and figures.

### Chapter 6: Experimental Design

**Current alignment:** Very strong. The failure-mode ladder is exactly the kind of design justification top AI/ML papers reward: each intervention maps to a hypothesis, and negative results become interpretable rather than anecdotal.

**Suggested refinement:** Keep the distinction between selected architecture and repair probes visually obvious. The main paper should not look like a collection of unrelated experiments; it should look like one frozen architecture plus a hypothesis-driven battery.

### Chapter 7: In-Domain Results

**Current alignment:** Strong. The chapter reports the architecture ladder, Top-3/Top-1 gap, verification retention, checker factorial, repair battery, backbone-size robustness, and confusion structure. It aligns with AI/ML standards because it includes ablations, paired tests, negative results, and robustness.

**Suggested refinement:** The narrative should repeatedly state what each result rules in or rules out. For example, retrieval improves the direct baseline, but the architecture's main contribution is auditability/error localization, not a robust extra Top-1 gain beyond retrieval.

### Chapter 8: External Validation and Configuration-Level Scope Expansion

**Current alignment:** Good, with one naming risk. The external MDD-5k evaluation is useful and the scope accounting is clear. The chapter correctly states that the result is synthetic transfer, not real-clinical validation.

**Suggested refinement:** Consider renaming the chapter or section from `External Validation` to `External Synthetic Evaluation` or `External Distribution-Shift Evaluation`. In clinical/IEEE health venues, the word `validation` can imply real-patient evidence unless qualified.

### Chapter 9: Error Archetypes and Worked Analyses

**Current alignment:** Good for a thesis and useful for interpretability-focused venues. The archetypes translate aggregate metrics into clinically meaningful failure modes.

**Suggested refinement:** Add one compact table mapping each archetype to the quantitative evidence that supports it. This would make the chapter easier to scan and more conference-like.

### Chapter 10: Discussion

**Current alignment:** Strong. The discussion is disciplined: it explains what decomposition achieves, why verification does not select, why simple repairs fail, and how to separate method limitation from modality limitation.

**Suggested refinement:** Reduce repetition with earlier chapters. Conference-style discussion should synthesize rather than restate. The strongest message is: the work is not a leaderboard claim; it is a failure-localization claim.

### Chapter 11: Limitations and Threats to Validity

**Current alignment:** Very strong. The limitations chapter is unusually careful and should satisfy reviewers concerned about synthetic data, pretraining overlap, internal split construction, metrics, unvalidated checker states, and non-clinical validity.

**Suggested refinement:** Move the most important limitation into the abstract/conclusion wording: synthetic corpora and no real-patient Taiwanese validation. The optimized abstract already does this through the phrase `not as clinically validated autonomous diagnosis`.

### Chapter 12: Clinical Deployment, Governance, and Human--AI Collaboration

**Current alignment:** Strong for IEEE/clinical AI readers; more expansive than a typical ACL conference paper. It correctly frames HiED as clinician-facing decision support and lists privacy, audit logging, human factors, fairness, clinical validation, monitoring, and regulation.

**Suggested refinement:** If converting to a conference paper, compress this chapter to a safety and deployment paragraph plus an ethics/governance appendix. For thesis defense, keep it.

### Chapter 13: Conclusions and Future Work

**Current alignment:** Good. The chapter answers research questions, summarizes the selection bottleneck, and gives a concrete future-work roadmap.

**Suggested refinement:** Keep the final conclusion close to the optimized abstract's final sentence. The same claim boundary should appear at the start and the end of the paper: auditable research architecture, selection bottleneck, no autonomous clinical validation.

### Appendices

**Current alignment:** Strong. Metrics, prompts/schemas, intervention details, worked traces, and experiment inventory improve reproducibility and reviewability.

**Suggested refinement:** Make sure every appendix item referenced in the main text has a stable label and that implementation artifacts or hashes are named where the thesis says they exist in the repository.

## Overall verdict

The manuscript is substantially aligned with top AI/ML and ACL expectations in evaluation discipline, ablation logic, negative-result framing, and claim boundaries. The main weakness was not the chapters; it was the abstract's emphasis. The revised abstract fixes that by making the paper's main contribution the controlled localization of failure across detection, verification, and selection.

The second weakness is length and repetition. The thesis form can keep the repetition, but a conference version should compress background, deployment, and some discussion while preserving the data/evaluation protocol, architecture, in-domain results, external distribution-shift results, and limitations.
