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
    r'3(?=[^\n]{0,160}chapter 8 group term)',
    '1',
    code,
)
if substitutions != 1:
    index = code.find('chapter 8 group term')
    context = code[max(0, index - 240): index + 80] if index >= 0 else 'label not found'
    raise RuntimeError(
        f'expected one chapter 8 count guard, changed {substitutions}; context={context!r}'
    )
exec(compile(code, '<apply_validity_repro_patch>', 'exec'))
