from pathlib import Path

if Path('school/main.tex').exists():
    target = Path('school/main.tex')
else:
    target = Path('paper/school/HiED_school_version.tex')

text = target.read_text(encoding='utf-8')
blocks = [
    r'''\paragraph{Answer to RQ3.}
Retrieval gives higher Top-1 point estimates for Single. The differences among the three HiED settings are smaller and depend on the split and measure.

''',
    r'''\paragraph{Answer to RQ1.}
TF--IDF with logistic regression is the strongest same-source classifier in this comparison. HiED and Single have almost identical Top-1 results.

''',
    r'''\paragraph{Answer to RQ2.}
Differences occur at more than one stage, but the largest group appears after the reference diagnosis is already present in the Top-3 and the compatible set.

''',
    r'''\paragraph{Answer to RQ4.}
None of the tested selection methods gives a clear and reliable improvement over DA.

''',
]
for block in blocks:
    if text.count(block) != 1:
        raise SystemExit(f'Expected one Chapter 6 answer block, found {text.count(block)}: {block[:50]}')
    text = text.replace(block, '')

for marker in ['Answer to RQ1.', 'Answer to RQ2.', 'Answer to RQ3.', 'Answer to RQ4.']:
    if marker in text:
        raise SystemExit(f'Repeated Chapter 6 answer remains: {marker}')

required = [
    '\\section{Chapter Summary}',
    'The internal results support four main conclusions.',
    '\\section{Answer to RQ5 and Chapter Summary}',
]
for item in required:
    if item not in text:
        raise SystemExit(f'Missing required summary after cleanup: {item}')

target.write_text(text, encoding='utf-8')
print(f'updated {target}')
