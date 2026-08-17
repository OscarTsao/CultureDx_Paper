from __future__ import annotations

import ast
import base64
import re
import zlib
from pathlib import Path

wrapper = Path('.github/scripts/rewrite_plain_language.py').read_text(encoding='utf-8')
match = re.search(r"b64decode\((?P<payload>'[^']+')\)", wrapper)
if not match:
    raise SystemExit('Compressed rewrite payload not found')
payload = ast.literal_eval(match.group('payload'))
source = zlib.decompress(base64.b64decode(payload)).decode('utf-8')
needle = '''    "genuine ranked Top-3 Accuracy": "Top-3 Accuracy",\n    "genuine Top-3 Accuracy": "Top-3 Accuracy",'''
replacement = '''    "Genuine ranked Top-3 Accuracy": "Top-3 Accuracy",\n    "Genuine Top-3 Accuracy": "Top-3 Accuracy",\n    "Genuine ranked Top-3": "Top-3",\n    "Genuine Top-3": "Top-3",\n    "genuine ranked Top-3 Accuracy": "Top-3 Accuracy",\n    "genuine Top-3 Accuracy": "Top-3 Accuracy",'''
if needle not in source:
    raise SystemExit('Top-3 replacement insertion point not found')
source = source.replace(needle, replacement)
exec(compile(source, '<rewrite_plain_language_v2>', 'exec'))
