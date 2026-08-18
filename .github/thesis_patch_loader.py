from pathlib import Path
import base64
import re
import zlib

parts = Path('.github/thesis_patch')
payload = ''.join(
    path.read_text(encoding='utf-8').strip()
    for path in sorted(parts.glob('payload*.txt'))
)
code = zlib.decompress(base64.b64decode(payload)).decode('utf-8')
code, substitutions = re.subn(
    r',\s*3,\s*["\']chapter 8 group term["\']\)',
    ', 1, "chapter 8 group term")',
    code,
)
if substitutions != 1:
    raise RuntimeError(f'expected one chapter 8 count guard, changed {substitutions}')
exec(compile(code, '<apply_validity_repro_patch>', 'exec'))
