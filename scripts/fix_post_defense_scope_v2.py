from pathlib import Path


def main() -> None:
    candidates = [Path("school/main.tex"), Path("paper/school/HiED_school_version.tex")]
    target = next((path for path in candidates if path.exists()), None)
    if target is None:
        raise FileNotFoundError("School thesis source not found")

    text = target.read_text(encoding="utf-8")
    comment_counts = (text.count("\\ct{"), text.count("\\wl{"))

    stale = (
        "Two ongoing studies provide complementary clinical evaluation outside the completed computational RQs: "
        "a blinded psychiatrist review of 20 selected LingxiDiag disagreement cases and a CGMH real-world validation. "
        "Because they use different populations and reference conditions, the two studies are analyzed separately."
    )
    replacement = (
        "The blinded psychiatrist annotation of 20 selected LingxiDiag disagreement cases is the only clinician-facing "
        "evaluation included in this thesis. It uses a selected synthetic disagreement sample and is analyzed separately "
        "from the completed computational RQs."
    )
    if stale not in text:
        raise RuntimeError("Expected obsolete clinical-scope paragraph was not found")
    text = text.replace(stale, replacement, 1)

    old_ack = (
        "guidance shaped the design of the differential-diagnosis framework,\n"
        "and the design of the psychiatrist annotation study for selected LingxiDiag cases. I am\n"
    )
    new_ack = (
        "guidance shaped both the differential-diagnosis framework and the\n"
        "psychiatrist annotation study for selected LingxiDiag cases. I am\n"
    )
    if old_ack not in text:
        raise RuntimeError("Expected acknowledgement text was not found")
    text = text.replace(old_ack, new_ack, 1)

    text = text.replace(
        "The only clinician-facing evaluation kept in this thesis is",
        "The only clinician-facing evaluation included in this thesis is",
    )
    text = text.replace("唯一保留的臨床人員評估", "唯一納入的臨床人員評估")

    if "CGMH" in text:
        raise RuntimeError("CGMH evaluation wording still remains in thesis")
    if (text.count("\\ct{"), text.count("\\wl{")) != comment_counts:
        raise RuntimeError("Advisor comment counts changed unexpectedly")

    target.write_text(text, encoding="utf-8")
    print(f"Updated {target}")


if __name__ == "__main__":
    main()
