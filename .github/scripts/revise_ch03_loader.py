from pathlib import Path
import base64
import zlib

parts = Path(".github/scripts/ch03_parts")
payload = "".join(
    part.read_text(encoding="utf-8").strip()
    for part in sorted(parts.glob("part*.txt"))
)
code = zlib.decompress(base64.b64decode(payload)).decode("utf-8")
exec(compile(code, "<revise_ch03>", "exec"))
