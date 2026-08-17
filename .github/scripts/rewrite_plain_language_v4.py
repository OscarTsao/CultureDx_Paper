from pathlib import Path
source = Path('.github/scripts/rewrite_plain_language_v3.py').read_text(encoding='utf-8')
source = source.replace("(r'post[- ]hoc', 'additional')", "(r'post[- ]?hoc', 'additional')")
exec(compile(source, '<rewrite_plain_language_v4>', 'exec'))
