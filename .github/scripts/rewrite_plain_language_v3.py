from __future__ import annotations

import ast
import base64
import re
import zlib
from pathlib import Path

wrapper = Path('.github/scripts/rewrite_plain_language.py').read_text(encoding='utf-8')
match = re.search(r"b64decode\((?P<payload>'[^']+')\)", wrapper)
if not match:
    raise SystemExit('Compressed rewrite payload not found')
payload = ast.literal_eval(match.group('payload'))
source = zlib.decompress(base64.b64decode(payload)).decode('utf-8')
needle = '''    "genuine ranked Top-3 Accuracy": "Top-3 Accuracy",\n    "genuine Top-3 Accuracy": "Top-3 Accuracy",'''
replacement = '''    "Genuine ranked Top-3 Accuracy": "Top-3 Accuracy",\n    "Genuine Top-3 Accuracy": "Top-3 Accuracy",\n    "Genuine ranked Top-3": "Top-3",\n    "Genuine Top-3": "Top-3",\n    "genuine ranked Top-3 Accuracy": "Top-3 Accuracy",\n    "genuine Top-3 Accuracy": "Top-3 Accuracy",'''
if needle not in source:
    raise SystemExit('Top-3 replacement insertion point not found')
source = source.replace(needle, replacement)

ns: dict[str, object] = {}
try:
    exec(compile(source, '<rewrite_plain_language_v3>', 'exec'), ns, ns)
except SystemExit:
    pass

text = ns.get('text')
target = ns.get('thesis')
if not isinstance(text, str) or not isinstance(target, Path):
    raise SystemExit('The structural rewrite did not produce thesis text')

for old, new in [
    ('Genuine ranked Top-3 Accuracy', 'Top-3 Accuracy'),
    ('Genuine Top-3 Accuracy', 'Top-3 Accuracy'),
    ('Ranked Top-3 Accuracy', 'Top-3 Accuracy'),
    ('genuine ranked Top-3 Accuracy', 'Top-3 Accuracy'),
    ('genuine Top-3 Accuracy', 'Top-3 Accuracy'),
    ('ranked Top-3 Accuracy', 'Top-3 Accuracy'),
    ('Genuine ranked Top-3', 'Top-3'),
    ('Genuine Top-3', 'Top-3'),
    ('Ranked Top-3', 'Top-3'),
    ('genuine ranked Top-3', 'Top-3'),
    ('genuine Top-3', 'Top-3'),
    ('ranked Top-3', 'Top-3'),
    ('Top-3 candidate coverage', 'Top-3 Accuracy'),
    ('Top-3 gold-label coverage', 'Top-3 Accuracy'),
    ('Top-3 coverage', 'Top-3 Accuracy'),
]:
    text = text.replace(old, new)

replacements = [
    (r'output and evaluation contracts?', 'stage-wise evaluation framework'),
    (r'evaluation contracts?', 'evaluation framework'),
    (r'output contracts?', 'output format'),
    (r'metric contracts?', 'metric definitions'),
    (r'scoring contracts?', 'scoring rules'),
    (r'ranking contracts?', 'ranking rules'),
    (r'evidence contracts?', 'information used'),
    (r'inference contracts?', 'model settings'),
    (r'parent-label contracts?', 'parent-label mapping'),
    (r'any-gold contracts?', 'any-gold scoring rule'),
    (r'study contracts?', 'study design'),
    (r'contracts?', 'rules'),
    (r'trace lineages?', 'saved runs'),
    (r'archived lineages?', 'saved runs'),
    (r'lineages?', 'saved runs'),
    (r'frozen snapshots?', 'saved results'),
    (r'frozen configurations?', 'selected configurations'),
    (r'frozen results?', 'saved results'),
    (r'frozen outputs?', 'saved outputs'),
    (r'frozen traces?', 'saved case-level results'),
    (r'matched traces?', 'matched case-level results'),
    (r'canonical-rescore traces?', 'separately recalculated results'),
    (r'case-level traces?', 'case-level results'),
    (r'upstream traces?', 'shared earlier outputs'),
    (r'full-pipeline', 'full-system'),
    (r'pipeline', 'system'),
    (r'traces?', 'saved results'),
    (r'artifact completeness', 'availability of saved results'),
    (r'source artifacts?', 'source files'),
    (r'recorded artifacts?', 'recorded outputs'),
    (r'upstream artifacts?', 'earlier outputs'),
    (r'artifacts?', 'saved outputs'),
    (r'provenance boundaries?', 'comparison limits'),
    (r'provenance', 'source information'),
    (r'post[- ]hoc', 'additional'),
    (r'forced-commit sweep', 'pairwise re-selection check'),
    (r'forced commit sweep', 'pairwise re-selection check'),
    (r'fixed-trace', 'saved-result'),
    (r'variant battery', 'set of methods'),
    (r'output cardinality', 'number of output diagnoses'),
    (r'inference budgets?', 'number of model calls'),
    (r'decoding contracts?', 'decoding settings'),
    (r'validation bundles?', 'validation results'),
]
for pattern, repl in replacements:
    text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

for old, new in [
    ('under the DA ranking rules', 'under the DA ranking rule'),
    ('under the recorded DA ranking rules', 'under the DA ranking rule'),
    ('using the thesis-wide any-gold scoring rule', 'using the same any-gold scoring rule'),
    ('the same any-gold scoring rule rule', 'the same any-gold scoring rule'),
    ('output format and three-label measures differ', 'available outputs differ'),
    ('complete output format', 'complete set of outputs'),
    ('stage-wise and inspectable output format', 'stage-wise and inspectable set of outputs'),
    ('a saved results', 'saved results'),
    ('the saved results is', 'the saved results are'),
]:
    text = text.replace(old, new)

forbidden = [
    r'\bcontract\b', r'\bcontracts\b', r'\blineage\b', r'\blineages\b',
    r'\bposthoc\b', r'emitted-label hit@3', r'genuine ranked Top-3',
    r'genuine Top-3', r'forced-commit sweep', r'frozen snapshot',
]
for pattern in forbidden:
    found = re.search(pattern, text, flags=re.IGNORECASE)
    if found:
        start = max(0, found.start() - 100)
        end = min(len(text), found.end() + 100)
        raise SystemExit(f'Forbidden wording remains: {pattern}\n{text[start:end]}')

required = [
    'Primary-diagnosis selection methods',
    'Run the Diagnostician $K$ times',
    'one advocate represents the diagnosis path',
    'criterion \\textit{met ratio}',
    '\\section{Proposed Psychiatrist Review}',
    '\\chapter{Internal Evaluation Results}',
    '\\chapter{External Synthetic Evaluation}',
]
for item in required:
    if item not in text:
        raise SystemExit(f'Missing required rewritten text: {item}')

for item in ['Trace-Lineage and Diagnostic-Scope Boundaries', 'fig:internal-external-gap', 'Evidence contract']:
    if item in text:
        raise SystemExit(f'Removed main-text item remains: {item}')

target.write_text(text, encoding='utf-8')
print(f'updated {target}')
