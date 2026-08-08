from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
TARGET = ROOT / "school" / "main.tex"
PART_DIR = ROOT / "scripts" / "ch7_tmp"
PARTS = [PART_DIR / f"part{i}.tex" for i in range(1, 5)]
START_MARKER = r"\chapter{External Synthetic Evaluation}"
END_MARKER = r"\chapter{Characterization of Recorded-Output Disagreements}"


def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(TARGET)
    for part in PARTS:
        if not part.exists():
            raise FileNotFoundError(part)

    text = TARGET.read_text(encoding="utf-8")
    chapter = "".join(part.read_text(encoding="utf-8") for part in PARTS).rstrip() + "\n\n"

    if text.count(START_MARKER) != 1 or text.count(END_MARKER) != 1:
        raise RuntimeError("Chapter 7 markers were not found exactly once")

    start = text.index(START_MARKER)
    end = text.index(END_MARKER, start)
    old_block = text[start:end]
    before_comments = (text.count(r"\ct{"), text.count(r"\wl{"))
    old_block_comments = (old_block.count(r"\ct{"), old_block.count(r"\wl{"))
    if old_block_comments != (0, 0):
        raise RuntimeError(f"Advisor comments found inside Chapter 7: {old_block_comments}")

    updated = text[:start] + chapter + text[end:]
    after_comments = (updated.count(r"\ct{"), updated.count(r"\wl{"))
    if before_comments != after_comments:
        raise RuntimeError("Advisor-comment counts changed unexpectedly")

    required = [
        r"\label{ch:external}",
        r"\label{tab:external-inventory}",
        r"\label{tab:external-summary-rewrite}",
        r"\label{fig:internal-external-gap}",
        r"\label{tab:external-disagreement-profiles}",
        r"\label{sec:mdd-multiway}",
        r"\label{tab:mdd-finalization-results}",
        r"\label{tab:scope-expansion-results}",
        r"\label{tab:lexical-transfer-rewrite}",
        "matched method-comparison trace",
        "225 cases (25.6\\%)",
        "0.786",
        "Posthoc fixed-trace forced-commit sweep",
        "0.059",
        "Answer to RQ5",
    ]
    missing = [item for item in required if item not in chapter]
    if missing:
        raise RuntimeError(f"Missing required Chapter 7 content: {missing}")

    forbidden = [
        "0.8907",
        "95.0\\%",
        "56.25\\%",
        "56.36\\%",
        "84.63\\%",
        "84.52\\%",
        "0.004",
        "0.096",
        "Forced pairwise override",
        "largely preserved across the source shift",
        "24,576",
        "top_k",
        "output budget",
        "serving setup",
    ]
    bad = [item for item in forbidden if item in chapter]
    if bad:
        raise RuntimeError(f"Obsolete or implementation-specific text remains in Chapter 7: {bad}")

    TARGET.write_text(updated, encoding="utf-8")
    print(f"Updated {TARGET}")
    print(f"Advisor comments preserved: CT={before_comments[0]}, WL={before_comments[1]}")


if __name__ == "__main__":
    main()
