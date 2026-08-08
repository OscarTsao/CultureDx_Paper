from __future__ import annotations

from pathlib import Path
import re

TARGET = Path("school/main.tex")
PART_DIR = Path("scripts/ch6_tmp")
START = r"\chapter{Internal Evaluation Results}"
END = r"\chapter{External Synthetic Evaluation}"


def main() -> None:
    parts = [PART_DIR / f"part{i}.tex" for i in range(1, 5)]
    missing_parts = [str(path) for path in parts if not path.is_file()]
    if missing_parts:
        raise FileNotFoundError(f"Missing Chapter 6 rewrite parts: {missing_parts}")

    replacement = "".join(path.read_text(encoding="utf-8") for path in parts).strip() + "\n\n"
    text = TARGET.read_text(encoding="utf-8")

    if text.count(START) != 1 or text.count(END) != 1:
        raise RuntimeError("Expected exactly one Chapter 6 marker and one Chapter 7 marker")
    start = text.index(START)
    end = text.index(END, start)
    old_chapter = text[start:end]
    if r"\ct{" in old_chapter or r"\wl{" in old_chapter:
        raise RuntimeError("Advisor comments were found inside Chapter 6; manual preservation is required")

    before_comments = (text.count(r"\ct{"), text.count(r"\wl{"))
    updated = text[:start] + replacement + text[end:]
    after_comments = (updated.count(r"\ct{"), updated.count(r"\wl{"))
    if before_comments != after_comments:
        raise RuntimeError(f"Advisor-comment counts changed: {before_comments} -> {after_comments}")

    labels = set(re.findall(r"\\label\{([^}]+)\}", updated))
    labels.update(
        re.findall(
            r"\\ThesisFigure(?:\[[^\]]*\])?\{[^{}]*\}\{.*?\}\{([^{}]+)\}",
            updated,
            flags=re.DOTALL,
        )
    )
    required_labels = {
        "ch:results",
        "sec:retrieval-results",
        "tab:retrieval-results",
        "sec:validation-retrieval-selection",
        "sec:matched-baselines-retrieval",
        "tab:matched-baselines-retrieval",
        "tab:validation-configuration-matrix",
        "sec:stage-wise-disagreement-results",
        "fig:selection-bottleneck",
        "sec:criterion-verification",
        "tab:d3rs-joint",
        "fig:d3rs-flow",
        "tab:oracle-headroom",
        "sec:nts-factorial",
        "sec:additional-selection-results",
        "tab:nts-factorial",
        "tab:internal-selection-results",
        "sec:model-scale-disagreement",
        "fig:size-robustness",
        "fig:confusion-thesis-rewrite",
    }
    missing_labels = sorted(required_labels - labels)
    if missing_labels:
        raise RuntimeError(f"Required labels missing after replacement: {missing_labels}")

    stale_text = [
        "Under the five-metric majority rule",
        "prespecified majority-based promotion rule",
        "Forced pairwise override & 0.443",
        "TF--IDF + LR versus HiED--DA & 229 & 115",
    ]
    present_stale = [item for item in stale_text if item in updated]
    if present_stale:
        raise RuntimeError(f"Stale or unsupported text remains: {present_stale}")

    new_end = updated.index(END, start)
    chapter = updated[start:new_end]
    implementation_terms = [
        "AWQ",
        "vLLM",
        "FAISS",
        "guided decoding",
        "JSON schema",
        "serving setup",
        "parse-recovery events",
    ]
    present_implementation = [item for item in implementation_terms if item in chapter]
    if present_implementation:
        raise RuntimeError(f"Implementation details remain in Chapter 6: {present_implementation}")

    required_phrases = [
        "Answer to RQ1",
        "Answer to RQ2",
        "Answer to RQ3",
        "Answer to RQ4",
        "Internal contribution to RQ5",
        "not estimates of clinical diagnostic accuracy",
        "all-five promotion condition",
    ]
    missing_phrases = [item for item in required_phrases if item not in chapter]
    if missing_phrases:
        raise RuntimeError(f"Required Chapter 6 phrases missing: {missing_phrases}")

    TARGET.write_text(updated, encoding="utf-8")
    print(f"Updated {TARGET}")
    print(f"Advisor comments preserved: CT={after_comments[0]}, WL={after_comments[1]}")


if __name__ == "__main__":
    main()
