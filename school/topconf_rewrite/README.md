# Top-conference narrative rewrite package

This directory contains complete rewritten LaTeX chapters for the main thesis body. These are not outlines or suggestions; each `chXX_*.tex` file is a complete replacement chapter written in a top AI/ML, ACL, and IEEE-style narrative while preserving thesis-level evidence depth.

## Files

- `ch01_introduction.tex`
- `ch02_background.tex`
- `ch03_related_work.tex`
- `ch04_data_evaluation.tex`
- `ch05_architecture.tex`
- `ch06_experimental_design.tex`
- `ch07_results.tex`
- `ch08_external.tex`
- `ch09_error_archetypes.tex`
- `ch10_discussion.tex`
- `ch11_limitations.tex`
- `ch12_deployment.tex`
- `ch13_conclusion.tex`
- `chapters_all.tex` includes all rewritten chapters in order.

## How to apply

Option A, safest review path:

1. Compare each rewritten chapter against the corresponding block in `school/main.tex`.
2. Replace one chapter at a time.
3. Compile after each replacement.
4. Keep original tables, figures, and appendix material if the advisor wants maximum thesis detail.

Option B, fast replacement path:

1. In `school/main.tex`, keep the preamble, front matter, table of contents, list of tables, and list of figures.
2. Replace the existing Chapter 1--13 block with:

```tex
\input{topconf_rewrite/chapters_all.tex}
```

3. Keep the existing appendices and bibliography after the included chapters.

## Abstracts

Use these replacement files for the front matter:

- `../abstract_zh_optimized_replacement.tex`
- `../abstract_optimized_replacement.tex`

Remove or hide visible mentor comments such as `\ct{Redo...}` in final builds.

## Narrative spine

The rewritten thesis is organized around one claim:

> HiED is not merely a psychiatric multi-agent system. It is an auditable experimental instrument showing that, under transcript-only evidence, the correct diagnosis can be detected and criterion-supported while still not being selected as the primary diagnosis.

## Notes

- Chapter 8 is renamed to `External Synthetic Evaluation and Configuration-Level Scope Transfer` to avoid implying real-patient clinical validation.
- The appendices are not rewritten here because they are mainly reproducibility and implementation material; they can remain in thesis style.
- Some labels include `-rewrite` suffixes to avoid collisions during side-by-side review. If these chapters replace the originals permanently, labels can be normalized.
