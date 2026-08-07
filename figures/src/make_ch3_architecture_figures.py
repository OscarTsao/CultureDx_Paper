from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


COLORS = {
    "panel": "#F7F7F7",
    "input": "#E8F3E8",
    "llm": "#FCE8D6",
    "det": "#E8E0F4",
    "artifact": "#FFFFFF",
    "final": "#DDEFF0",
    "missing": "#FFF4CC",
    "ink": "#202020",
    "muted": "#666666",
}


def _box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    *,
    face: str = "artifact",
    edge: str = "ink",
    linewidth: float = 1.4,
    linestyle: str = "-",
    fontsize: float = 9.2,
    weight: str = "normal",
    align: str = "center",
    pad: float = 0.012,
    zorder: int = 2,
):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad={pad},rounding_size=0.012",
        facecolor=COLORS.get(face, face),
        edgecolor=COLORS.get(edge, edge),
        linewidth=linewidth,
        linestyle=linestyle,
        zorder=zorder,
    )
    ax.add_patch(patch)
    ha = {"center": "center", "left": "left", "right": "right"}[align]
    tx = x + w / 2 if align == "center" else x + 0.02 if align == "left" else x + w - 0.02
    ax.text(
        tx,
        y + h / 2,
        text,
        ha=ha,
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        color=COLORS["ink"],
        linespacing=1.25,
        zorder=zorder + 1,
    )
    return patch


def _arrow(
    ax,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    dashed: bool = False,
    color: str = "ink",
    linewidth: float = 1.35,
    mutation_scale: float = 13,
    zorder: int = 3,
):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation_scale,
        linewidth=linewidth,
        linestyle="--" if dashed else "-",
        color=COLORS.get(color, color),
        shrinkA=2,
        shrinkB=2,
        zorder=zorder,
    )
    ax.add_patch(arrow)
    return arrow


def _save(fig, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "Title": output.stem,
        "Author": "HiED thesis",
        "Creator": "make_ch3_architecture_figures.py",
        "Producer": "Matplotlib",
        "CreationDate": None,
        "ModDate": None,
    }
    fig.savefig(output, bbox_inches="tight", metadata=metadata)
    plt.close(fig)


def make_single_vs_hied(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(13.2, 7.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Panel backgrounds
    _box(ax, 0.02, 0.05, 0.32, 0.90, "", face="panel", linewidth=1.2, zorder=0)
    _box(ax, 0.37, 0.05, 0.61, 0.90, "", face="panel", linewidth=1.2, zorder=0)
    ax.text(0.04, 0.925, "A. Single LLM baseline", fontsize=13.2, fontweight="bold", va="top")
    ax.text(0.39, 0.925, "B. HiED two-path architecture", fontsize=13.2, fontweight="bold", va="top")

    # Single panel
    _box(ax, 0.08, 0.78, 0.20, 0.09, "Fixed transcript", face="input", weight="bold")
    _box(
        ax,
        0.08,
        0.65,
        0.20,
        0.08,
        "Optional similar cases",
        face="artifact",
        linestyle="--",
        fontsize=8.8,
    )
    _box(ax, 0.09, 0.45, 0.18, 0.12, "Single LLM", face="llm", weight="bold", fontsize=11)
    _box(
        ax,
        0.055,
        0.20,
        0.25,
        0.16,
        "Recorded final outputs\n\nPrimary diagnosis\nOptional emitted labels",
        face="artifact",
        linestyle="--",
        fontsize=9.2,
        weight="bold",
    )
    _arrow(ax, (0.18, 0.78), (0.18, 0.57))
    _arrow(ax, (0.18, 0.65), (0.18, 0.57), dashed=True)
    _arrow(ax, (0.18, 0.45), (0.18, 0.36))
    ax.text(
        0.18,
        0.13,
        "No standardized ranked differential or\ndiagnosis-specific criterion record\nunder the evaluated output contract",
        ha="center",
        va="center",
        fontsize=8.4,
        color=COLORS["muted"],
        style="italic",
        linespacing=1.25,
    )

    # HiED shared inputs
    _box(ax, 0.56, 0.80, 0.22, 0.08, "Fixed transcript", face="input", weight="bold")
    _box(
        ax,
        0.39,
        0.69,
        0.18,
        0.07,
        "Optional similar cases",
        face="artifact",
        linestyle="--",
        fontsize=8.4,
    )

    ax.text(0.47, 0.655, "Diagnosis path", fontsize=10.5, fontweight="bold", ha="center")
    ax.text(0.82, 0.655, "Criterion-checking path", fontsize=10.5, fontweight="bold", ha="center")
    _box(ax, 0.405, 0.53, 0.20, 0.10, "Diagnostician", face="llm", weight="bold", fontsize=10.4)
    _box(
        ax,
        0.69,
        0.50,
        0.24,
        0.13,
        "Diagnosis-specific\nCriterion Checkers\n\nAll 14 configured categories",
        face="llm",
        weight="bold",
        fontsize=9.2,
    )
    _box(
        ax,
        0.39,
        0.28,
        0.23,
        0.18,
        "Recorded diagnosis outputs\n\nRanked candidates (up to 5)\nProposed primary\nOptional comorbid diagnosis",
        face="artifact",
        linestyle="--",
        fontsize=8.8,
        weight="bold",
    )
    _box(
        ax,
        0.685,
        0.31,
        0.25,
        0.13,
        "Criterion states\n\nmet  |  not_met\ninsufficient_evidence",
        face="artifact",
        linestyle="--",
        fontsize=8.8,
        weight="bold",
    )
    _box(
        ax,
        0.705,
        0.17,
        0.21,
        0.085,
        "Compatibility Auditor",
        face="det",
        linewidth=2.1,
        weight="bold",
        fontsize=9.1,
    )
    _box(
        ax,
        0.695,
        0.065,
        0.23,
        0.065,
        "Criterion-compatible set",
        face="artifact",
        linestyle="--",
        fontsize=8.7,
        weight="bold",
    )
    _box(
        ax,
        0.455,
        0.085,
        0.19,
        0.095,
        "Finalization policy\nDA or NtS",
        face="det",
        linewidth=2.1,
        weight="bold",
        fontsize=9.0,
    )
    _box(
        ax,
        0.39,
        0.015,
        0.25,
        0.05,
        "Committed primary diagnosis",
        face="final",
        linewidth=2.5,
        weight="bold",
        fontsize=8.8,
    )

    # HiED arrows
    _arrow(ax, (0.64, 0.80), (0.51, 0.63))
    _arrow(ax, (0.70, 0.80), (0.81, 0.63))
    _arrow(ax, (0.48, 0.69), (0.50, 0.63), dashed=True)
    _arrow(ax, (0.505, 0.53), (0.505, 0.46))
    _arrow(ax, (0.81, 0.50), (0.81, 0.44))
    _arrow(ax, (0.81, 0.31), (0.81, 0.255))
    _arrow(ax, (0.81, 0.17), (0.81, 0.13))
    _arrow(ax, (0.62, 0.31), (0.57, 0.18))
    _arrow(ax, (0.695, 0.10), (0.645, 0.13))
    _arrow(ax, (0.55, 0.085), (0.52, 0.065))

    ax.text(
        0.675,
        0.97,
        "Same fixed transcript; different recorded output contracts",
        ha="center",
        va="top",
        fontsize=10,
        color=COLORS["muted"],
        style="italic",
    )

    _save(fig, output)


def make_worked_example(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(12.2, 10.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    _box(
        ax,
        0.16,
        0.90,
        0.68,
        0.075,
        "Complete constructed transcript\nIllustrative case — not a patient record or exported model trace",
        face="input",
        linewidth=1.8,
        weight="bold",
        fontsize=10.2,
    )

    ax.text(0.25, 0.855, "Diagnosis path", fontsize=11.2, fontweight="bold", ha="center")
    ax.text(0.73, 0.855, "Criterion-checking path", fontsize=11.2, fontweight="bold", ha="center")

    _box(ax, 0.13, 0.73, 0.24, 0.095, "Diagnostician", face="llm", weight="bold", fontsize=10.6)
    _box(
        ax,
        0.055,
        0.48,
        0.39,
        0.20,
        "Illustrative ranked candidates\n\n1. F41.1 Generalized anxiety disorder\n2. F32 Depressive episode\n3. F51 Nonorganic sleep disorder\n\nProposed primary: F41.1\nOptional comorbidity: None",
        face="artifact",
        linestyle="--",
        weight="bold",
        fontsize=8.7,
        align="left",
    )
    ax.text(
        0.25,
        0.455,
        "Up to five candidates may be retained; only the leading three are shown.",
        ha="center",
        va="top",
        fontsize=7.7,
        color=COLORS["muted"],
        style="italic",
    )

    _box(
        ax,
        0.59,
        0.72,
        0.28,
        0.105,
        "Diagnosis-specific\nCriterion Checkers\n\nAll 14 categories checked",
        face="llm",
        weight="bold",
        fontsize=9.4,
    )
    _box(
        ax,
        0.51,
        0.57,
        0.22,
        0.12,
        "F32\n\nCore symptoms: met\nDuration: met\nAssociated symptoms: met\n\nIncluded",
        face="artifact",
        linestyle="--",
        weight="bold",
        fontsize=8.2,
        align="left",
    )
    _box(
        ax,
        0.75,
        0.54,
        0.22,
        0.15,
        "F41.1\n\nMulti-area worry: met\nRequired duration:\ninsufficient_evidence\nAssociated symptoms:\ninsufficient_evidence\n\nNot included",
        face="artifact",
        linestyle="--",
        weight="bold",
        fontsize=7.7,
        align="left",
    )
    _box(
        ax,
        0.60,
        0.40,
        0.24,
        0.095,
        "F31\n\nPrevious manic episode: not_met\n\nNot included",
        face="artifact",
        linestyle="--",
        weight="bold",
        fontsize=8.2,
        align="left",
    )
    _box(
        ax,
        0.61,
        0.28,
        0.22,
        0.075,
        "Compatibility Auditor",
        face="det",
        linewidth=2.1,
        weight="bold",
        fontsize=9.0,
    )
    _box(
        ax,
        0.62,
        0.19,
        0.20,
        0.055,
        "Compatible set: {F32}",
        face="artifact",
        linestyle="--",
        weight="bold",
        fontsize=8.6,
    )

    # Data flow arrows
    _arrow(ax, (0.43, 0.90), (0.25, 0.825))
    _arrow(ax, (0.57, 0.90), (0.73, 0.825))
    _arrow(ax, (0.25, 0.73), (0.25, 0.68))
    _arrow(ax, (0.73, 0.72), (0.62, 0.69))
    _arrow(ax, (0.73, 0.72), (0.86, 0.69))
    _arrow(ax, (0.73, 0.72), (0.72, 0.495))
    _arrow(ax, (0.72, 0.40), (0.72, 0.355))
    _arrow(ax, (0.72, 0.28), (0.72, 0.245))

    ax.text(
        0.50,
        0.395,
        "Same transcript and same recorded upstream outputs",
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color=COLORS["muted"],
    )
    _arrow(ax, (0.31, 0.48), (0.34, 0.29))
    _arrow(ax, (0.62, 0.22), (0.57, 0.29))

    _box(
        ax,
        0.08,
        0.16,
        0.36,
        0.105,
        "Direct-Answer\n\nKeep the proposed primary\n\nCommitted primary: F41.1",
        face="final",
        linewidth=2.3,
        weight="bold",
        fontsize=9.3,
    )
    _box(
        ax,
        0.56,
        0.16,
        0.36,
        0.105,
        "Nominate-then-Select\n\nChoose the highest-ranked compatible candidate\n\nCommitted primary: F32",
        face="final",
        linewidth=2.3,
        weight="bold",
        fontsize=9.1,
    )
    _arrow(ax, (0.34, 0.29), (0.26, 0.265))
    _arrow(ax, (0.57, 0.29), (0.74, 0.265))

    _box(
        ax,
        0.20,
        0.045,
        0.60,
        0.075,
        "Important missing information\nOnset and duration of the anxiety symptoms remain unclear",
        face="missing",
        linestyle=":",
        linewidth=2.0,
        weight="bold",
        fontsize=9.4,
    )

    _save(fig, output)


def main() -> None:
    if Path("school/main.tex").exists():
        out_dir = Path("figures")
    elif Path("paper/school/HiED_school_version.tex").exists():
        out_dir = Path("paper/figures")
    else:
        raise FileNotFoundError("Could not identify the School thesis repository layout")

    make_single_vs_hied(out_dir / "fig_single_vs_hied_architecture.pdf")
    make_worked_example(out_dir / "fig_worked_example_flow.pdf")
    print(f"Generated Chapter 3 figures in {out_dir}")


if __name__ == "__main__":
    main()
