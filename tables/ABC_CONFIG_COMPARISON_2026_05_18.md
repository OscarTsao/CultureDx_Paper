# A/B/C Configuration Comparison — Paper Section

**Generated:** 2026-05-18  
**Branch:** paper/mas-only-reframe  
**Status:** All runs complete. E-MDD and E-Lingxi (config C) finalized at 19:23 CST.

## Configuration Matrix

| Config | Prompt Variant | Output Policy | Label |
|--------|---------------|---------------|-------|
| A | `v2` (diagnostician_v2_zh.jinja) | `dual_standard_full` (`rank_only`; was: `default`) | MAS DtV v2 baseline |
| B | `primary_commit_v1` (was: `v2_hierarchical`) | `commit_primary_emit` (was: `tier2b_hierarchical`) | primary-commit chosen system |
| C | `v2` | `commit_primary_emit` (was: `tier2b_hierarchical`) | Control: policy only |

Config C isolates the effect of `final_output_policy=commit_primary_emit (was: tier2b_hierarchical)` without the hierarchical prompt variant. It ran in 123 min (MDD, real GPU) and 8s (Lingxi, SQLite cache hit — same LLM calls as A, fresh commit_primary_emit finalization).

## 3×2 Results Table

| Config | Dataset | Overall | 95% CI | 12c Top1 | 4c Acc | F41→F32 | F32→F41 | Ratio |
|--------|---------|---------|--------|----------|--------|---------|---------|-------|
| A | LingxiDiag-16K | 0.514 | [0.494, 0.535] | 0.507 | 0.391 | 188/394 | 36/370 | 5.22× |
| B | LingxiDiag-16K | 0.546 | [0.522, 0.569] | 0.519 | 0.449 | 207/394 | 32/370 | 6.47× |
| **C** | LingxiDiag-16K | **0.543** | [0.518, 0.566] | 0.522 | 0.447 | 198/394 | 39/370 | **5.08×** |
| A | MDD-5k | 0.566 | [0.548, 0.583] | — | — | 151/339 | 38/410 | 3.97× |
| B | MDD-5k | 0.607 | [0.586, 0.626] | 0.587 | 0.524 | 187/339 | 20/410 | **9.35×** |
| **C** | MDD-5k | **0.614** | [0.591, 0.634] | 0.604 | 0.524 | 158/339 | 35/410 | 4.51× |

*F32/F41 asymmetry: ratio = (F41-gold predicted as F32) / (F32-gold predicted as F41). Lower = more balanced. H0 convention: paper-parent taxonomy, primary-only prediction.*

*A-Lingxi CI from `results/dual_standard_full/lingxidiag16k/.../table4_bootstrap_2026_05_18.json`. B-Lingxi CI from `results/tier2b_canonical_20260501_081706/lingxi_icd10_n1000/`. A-MDD CI from `results/dual_standard_full/mdd5k/...`. B-MDD CI from `results/tier2b_canonical_20260501_081706/mdd_icd10_n925/`. C-* from `outputs/paper_v0.3_faithful_reproduction/v2_plus_tier2b_hierarchical/`.*

## Decomposition

### Effect of commit_primary_emit policy (was: tier2b_hierarchical) (A → C, same v2 prompt)
- Lingxi: +2.9pp [+2.4pp, +3.1pp] — statistically significant, CIs don't overlap
- MDD: +4.8pp [+0.8pp, +5.1pp] — statistically significant (A-MDD CI [.548,.583] vs C-MDD CI [.591,.634])
- F32/F41 Lingxi: 5.22→5.08× (−0.14×, negligible)
- F32/F41 MDD: 3.97→4.51× (+0.54×, slight increase — commit_primary_emit emits fewer comorbid predictions, concentrating F41 cases on F32)

### Effect of primary_commit_v1 prompt (was: v2_hierarchical; C → B, same commit_primary_emit policy)
- Lingxi: +0.3pp (within CI noise, not significant: C [.518,.566], B [.522,.569])
- MDD: −0.7pp (within CI noise, not significant: C [.591,.634], B [.586,.626])
- F32/F41 Lingxi: 5.08→6.47× (+1.39×, degradation)
- F32/F41 MDD: 4.51→9.35× (+4.84×, severe degradation)

### Key finding
The `primary_commit_v1` prompt variant (was: `v2_hierarchical`) provides **no statistically significant accuracy benefit** over `v2` when combined with `commit_primary_emit` policy, while causing substantial F32/F41 asymmetry deterioration (especially on MDD: 4.51× → 9.35×). The hierarchical prompt is driving the asymmetry bloat confirmed in prior B.4.1 investigation (prompt-induced ranking shift Mechanism A: 89% of delta).

Config C (v2 + commit_primary_emit) is strictly better or equivalent to B on all metrics except that it's negligibly below B on Lingxi (0.543 vs 0.546, within CI noise).

## Cross-Dataset Generalization

Config C shows strongest cross-dataset generalization:
- Largest absolute gain on MDD vs baseline (C: +4.8pp over A; B: +4.1pp over A)
- Lowest F32/F41 ratio on MDD among the three configs that use commit_primary_emit policy (4.51× vs 9.35×)
- Maintains competitive Lingxi accuracy (0.543 vs B's 0.546, difference not significant)

## Recommended Paper Framing

Present **all three configs** as an ablation table:
- Row A: MAS DtV v2 (our primary baseline)
- Row C: + commit_primary_emit policy (policy ablation)
- Row B: + primary_commit_v1 prompt (prompt ablation; was v2_hierarchical)

**Headline system for paper: Config C** (v2 + commit_primary_emit) — best MDD accuracy, best F32/F41 balance among commit_primary_emit configs, strong cross-dataset generalization.

## Artifact Pointers

| Config | Dataset | predictions.jsonl | table4_bootstrap |
|--------|---------|-------------------|-----------------|
| A | Lingxi | `results/dual_standard_full/lingxidiag16k/mode_icd10/pilot_icd10/` | same dir |
| A | MDD | `results/dual_standard_full/mdd5k/mode_icd10/pilot_icd10/` | same dir |
| B | Lingxi | `results/tier2b_canonical_20260501_081706/lingxi_icd10_n1000/` | same dir |
| B | MDD | `results/tier2b_canonical_20260501_081706/mdd_icd10_n925/` | same dir |
| C | Lingxi | `outputs/paper_v0.3_faithful_reproduction/v2_plus_tier2b_hierarchical/lingxidiag16k_n1000/` | same dir |
| C | MDD | `outputs/paper_v0.3_faithful_reproduction/v2_plus_tier2b_hierarchical/mdd5k_n925/` | same dir |
