from pathlib import Path
import re

source = Path('.github/scripts/rewrite_plain_language_v3.py').read_text(encoding='utf-8')
source = source.replace("(r'post[- ]hoc', 'additional')", "(r'post[- ]?hoc', 'additional')")
source = source.replace("'one advocate represents the diagnosis path'", "'One advocate represents the diagnosis path'")
exec(compile(source, '<rewrite_plain_language_v4>', 'exec'))

for target in [Path('school/main.tex'), Path('paper/school/HiED_school_version.tex')]:
    if not target.exists():
        continue
    text = target.read_text(encoding='utf-8')
    text = text.replace('fig_system_round20c', 'fig_pipeline_round20c')

    # Plain-language substitutions may change words inside LaTeX labels and
    # references. Keep those identifiers valid and matched by replacing any
    # introduced spaces with hyphens in both definitions and uses.
    def clean_identifier(match: re.Match[str]) -> str:
        command = match.group(1)
        value = re.sub(r'\s+', '-', match.group(2).strip())
        return f'\\{command}{{{value}}}'

    text = re.sub(
        r'\\(label|ref|pageref|autoref|cref|Cref)\{([^{}]+)\}',
        clean_identifier,
        text,
    )
    target.write_text(text, encoding='utf-8')
