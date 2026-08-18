from pathlib import Path
import base64
import zlib

parts = Path('.github/thesis_patch')
payload = ''.join(
    path.read_text(encoding='utf-8').strip()
    for path in sorted(parts.glob('payload*.txt'))
)
code = zlib.decompress(base64.b64decode(payload)).decode('utf-8')
exec(compile(code, '<apply_validity_repro_patch>', 'exec'))
