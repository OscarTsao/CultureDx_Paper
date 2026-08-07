from __future__ import annotations

import re
from pathlib import Path


def main() -> None:
    candidates = [Path("school/main.tex"), Path("paper/school/HiED_school_version.tex")]
    target = next((path for path in candidates if path.exists()), None)
    if target is None:
        raise FileNotFoundError("School thesis source not found")

    text = target.read_text(encoding="utf-8")
    comment_counts = (text.count("\\ct{"), text.count("\\wl{"))

    repaired, count = re.subn(
        r"Section~\s*ef\{sec:clinical-evaluation-plan\}",
        r"Section~\\ref{sec:clinical-evaluation-plan}",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"Expected exactly one malformed LaTeX reference; found {count}")

    if "Section~\\ref{sec:clinical-evaluation-plan}" not in repaired:
        raise RuntimeError("Corrected LaTeX reference was not written")
    if re.search(r"Section~\s*ef\{sec:clinical-evaluation-plan\}", repaired):
        raise RuntimeError("Malformed LaTeX reference remains")
    if (repaired.count("\\ct{"), repaired.count("\\wl{")) != comment_counts:
        raise RuntimeError("Advisor comment counts changed unexpectedly")

    target.write_text(repaired, encoding="utf-8")
    print(f"Repaired {target}")


if __name__ == "__main__":
    main()
