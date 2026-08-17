from pathlib import Path
source = Path('.github/scripts/rewrite_plain_language_v3.py').read_text(encoding='utf-8')
source = source.replace("(r'post[- ]hoc', 'additional')", "(r'post[- ]?hoc', 'additional')")
source = source.replace("'one advocate represents the diagnosis path'", "'One advocate represents the diagnosis path'")
exec(compile(source, '<rewrite_plain_language_v4>', 'exec'))
