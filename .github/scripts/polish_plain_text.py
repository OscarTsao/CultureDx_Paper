from pathlib import Path

if Path('school/main.tex').exists():
    target = Path('school/main.tex')
else:
    target = Path('paper/school/HiED_school_version.tex')

text = target.read_text(encoding='utf-8')

replacements = {
    'The compiled thesis inserts the figure output.': 'The figure file is missing.',
    "HiED therefore does not establish superior final-label accuracy. Its main contribution is a stage-wise evaluation framework that records the same outputs for every case that makes candidate omission, criterion incompatibility, missing information, and primary-selection disagreement separately inspectable.": "HiED therefore does not establish superior final-label accuracy. Its main contribution is a stage-wise evaluation framework that records the same outputs for every case. This makes candidate omission, criterion incompatibility, missing information, and primary-selection disagreement separately visible.",
    'Standardized ranked differential & Not produced under this rules': 'Standardized ranked differential & Not produced',
    'A difference between their final primary diagnoses can be saved resultsd to the finalization policy rather than to a different transcript, a different candidate ranking, or a different criterion-checking result.': 'Because the earlier outputs are the same, any difference in the final primary diagnosis comes from the final selection rule.',
    'Choose among eligible candidates using the criterion \\textit{met ratio}; ranking is used when needed': 'Select the eligible diagnosis with the highest criterion \\textit{met ratio}',
    'The analysis uses one frozen 1,000-case internal held-out results.': 'The analysis uses the saved case-level results from the 1,000-case internal held-out set.',
    'in this saved results': 'in these saved results',
    '\\paragraph{Frozen-record examples.}': '\\paragraph{Selected examples.}',
    'individual frozen records': 'individual saved records',
    '\\section{Selected Frozen-Output Examples}': '\\section{Selected Output Examples}',
    'same frozen internal case-level results': 'same internal case-level results',
    'frozen ontology used by the rule engine': 'fixed study rule set',
    'saved case-level results contains': 'saved case-level results contain',
    'The frequency of this profile differs across datasets and archived saved results.': 'The frequency of this profile differs across datasets and saved runs.',
    'These results identify several separate problems---candidate absence, broad or saved results-sensitive compatibility, primary-diagnosis selection, complete-set construction, diagnostic scope, and source-specific prediction.': 'These results identify several separate problems: missing candidates, broad compatibility rules, primary-diagnosis selection, complete-set construction, diagnostic scope, and source-specific prediction.',
    'HiED preserves a ranked differential, criterion states, short evidence notes, a criterion-compatible set, and the finalization source.': 'HiED preserves a ranked differential, criterion states, short evidence notes, a criterion-compatible set, and a record of the final selection.',
    'MDD-5k provides a second synthetic source, not a clinical cohort. The archived MDD-5k outputs also contain more than one saved run. The matched method-comparison saved results, canonical rescore, and historical output are not interchangeable. The main external claims use one matched case-level results, while the canonical saved results is reported only as sensitivity evidence. Mixing fields across these saved results would not reproduce one system run.': 'MDD-5k provides a second synthetic source, not a clinical cohort. More than one saved MDD-5k run exists, and their outputs differ. The main external results use one matched set of case-level outputs. A separate recalculation is used only as a sensitivity check. Outputs from different runs are not combined.',
    'No supported quantitative conclusion is drawn from the earlier F60 scope-expansion experiment because its source file was not preserved in the saved repository results.': 'No supported quantitative conclusion is drawn from the earlier F60 scope-expansion experiment because the source results were not preserved.',
    '\\section{Statistical, saved outputs, and Reproducibility Limitations}': '\\section{Statistical and Reproducibility Limitations}',
    'availability of saved results also differs across analyses. The internal HiED headline row, the internal $D_3/I/S$ profiles, the paired DA--NtS comparison, and the matched external case-level results have case-level support. Several baseline and supporting results remain available only as aggregate summaries or incomplete records. These results cannot support new paired confidence intervals, case-overlap claims, or claims about which individual cases changed.': 'Case-level outputs are available for the main HiED result, the internal $D_3/I/S$ groups, the DA--NtS comparison, and the main external analysis. Some baseline and supporting results are available only as summary values. Those results cannot support new paired confidence intervals or case-by-case comparisons.',
    "HiED's completed technical contribution": "HiED's main contribution",
    'matched MDD-5k saved results': 'main MDD-5k evaluation',
    'preserved saved results': 'saved results',
    'archived MDD-5k runs': 'saved MDD-5k runs',
    'genuine ranked differential': 'Top-3 diagnoses',
    'The complete machine-readable criterion definitions, prompts, and rule-engine configuration remain in the versioned project repository.': 'The full criterion definitions and prompts are available in the project files.',
    'It does not repeat the complete software implementation. Full prompts, case-level outputs, seed schedules, evaluation scripts, and executable configurations remain in the versioned project repository.': 'This appendix summarizes the settings needed to understand the supporting experiments. Full project files are stored separately.',
    'additional pairwise re-selection check': 'Pairwise re-selection check',
    'Fixed-saved results policy replay; not a separately executed model configuration and not reported as an internal result.': 'Reuses saved pairwise choices; not a separate model run and not reported as an internal result.',
    'saved DA saved results': 'saved DA results',
    'The additional forced-commit result is different. It replays valid preferences already stored in the matched MDD-5k pairwise saved results and adds no model call. It is not a separately executed system, and no matching internal result is reported.': 'A separate pairwise re-selection check reuses saved pairwise choices without another model call. It is not a separate system run, and no matching internal result is reported.',
    'matched MDD-5k pairwise saved results': 'saved MDD-5k pairwise results',
    'Detailed external paired-test results on the common 925-case MDD-5k saved results.': 'Detailed external paired-test results on the same 925 MDD-5k cases.',
}

for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new)

for forbidden in [
    'saved resultsd', 'under this rules', 'archived saved results',
    'one matched case-level results', 'canonical saved results is',
    'availability of saved results', 'frozen ontology',
    'Frozen-record examples', 'Selected Frozen-Output Examples',
    'saved DA saved results', 'broad or saved results-sensitive',
]:
    if forbidden in text:
        raise SystemExit(f'Unpolished wording remains: {forbidden}')

required = [
    'Select the eligible diagnosis with the highest criterion \\textit{met ratio}',
    'Run the Diagnostician $K$ times, with $K=3$ or $5$, and use majority voting',
    'One advocate represents the diagnosis path and one represents the criterion path; after their debate, a judge agent selects the final diagnosis',
    '\\section{Statistical and Reproducibility Limitations}',
]
for phrase in required:
    if phrase not in text:
        raise SystemExit(f'Missing polished phrase: {phrase}')

target.write_text(text, encoding='utf-8')
print(f'polished {target}')
