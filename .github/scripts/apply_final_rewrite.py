from pathlib import Path
import base64
import zlib

parts_dir = Path('.github/scripts/final_rewrite_parts')
part_files = sorted(parts_dir.glob('part*.txt'))
if len(part_files) != 8:
    raise SystemExit(f'Expected 8 payload parts, found {len(part_files)}')
payload = ''.join(part.read_text(encoding='utf-8').strip() for part in part_files)
code = zlib.decompress(base64.b64decode(payload)).decode('utf-8')
exec(compile(code, '<apply_final_rewrite>', 'exec'))
