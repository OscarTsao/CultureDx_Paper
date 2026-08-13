from pathlib import Path

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


def box(
    ax,
    x,
    y,
    w,
    h,
    text,
    face="artifact",
    edge="ink",
    linewidth=1.4,
    linestyle="-",
    fontsize=9.2,
    weight="normal",
    align="center",
    pad=0.009,
    zorder=2,
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
    tx = x + w / 2 if align == "center" else x + 0.018
    ax.text(
        tx,
        y + h / 2,
        text,
        ha=align,
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        color=COLORS["ink"],
        linespacing=1.18,
        zorder=zorder + 1,
    )
    return patch


def arrow(
    ax,
    start,
    end,
    dashed=False,
    color="ink",
    linewidth=1.3,
    mutation_scale=12,
    zorder=3,
    rad=0,
):
    patch = FancyArrowPatch(
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
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(patch)
    return patch


def save(fig, path: Path) -> None:
    fig.savefig(
        path,
        bbox_inches="tight",
        metadata={"CreationDate": None, "ModDate": None},
    )
    plt.close(fig)


def make_hied_two_path_architecture(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(13.8, 8.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.975,
        "HiED: stage-wise diagnostic workflow and recorded outputs",
        ha="center",
        va="top",
        fontsize=14.0,
        fontweight="bold",
        color=COLORS["ink"],
    )

    box(
        ax,
        0.34,
        0.875,
        0.32,
        0.065,
        "Fixed speaker-labeled psychiatric interview transcript",
        face="input",
        linewidth=1.8,
        weight="bold",
        fontsize=9.6,
    )
    box(
        ax,
        0.055,
        0.805,
        0.22,
        0.052,
        "Optional similar cases\n(training examples)",
        linestyle="--",
        fontsize=8.4,
    )
    box(
        ax,
        0.725,
        0.805,
        0.22,
        0.052,
        "Criteria for 14 configured\ndiagnostic categories",
        linestyle="--",
        fontsize=8.4,
    )

    box(ax, 0.035, 0.405, 0.435, 0.365, "", face="panel", linewidth=1.2, zorder=0)
    box(ax, 0.53, 0.405, 0.435, 0.365, "", face="panel", linewidth=1.2, zorder=0)
    ax.text(0.055, 0.744, "1. Diagnosis path", fontsize=12.2, fontweight="bold", va="top")
    ax.text(0.55, 0.744, "2. Criterion-checking path", fontsize=12.2, fontweight="bold", va="top")

    box(
        ax,
        0.135,
        0.625,
        0.235,
        0.08,
        "Diagnostician",
        face="llm",
        linewidth=1.8,
        weight="bold",
        fontsize=10.4,
    )
    box(
        ax,
        0.085,
        0.445,
        0.335,
        0.135,
        "Recorded diagnosis outputs\n\nRanked candidates (up to five)\nProposed primary diagnosis\nOptional comorbid diagnosis",
        linestyle="--",
        weight="bold",
        fontsize=8.6,
    )

    box(
        ax,
        0.63,
        0.615,
        0.235,
        0.095,
        "Diagnosis-specific\nCriterion Checkers",
        face="llm",
        linewidth=1.8,
        weight="bold",
        fontsize=9.5,
    )
    box(
        ax,
        0.575,
        0.465,
        0.345,
        0.11,
        "Recorded criterion information\n\nmet  |  not_met  |  insufficient_evidence\nShort evidence notes and missing information",
        linestyle="--",
        weight="bold",
        fontsize=8.1,
    )
    box(
        ax,
        0.645,
        0.405,
        0.205,
        0.048,
        "Compatibility Auditor",
        face="det",
        linewidth=1.8,
        weight="bold",
        fontsize=8.8,
    )
    box(
        ax,
        0.635,
        0.335,
        0.225,
        0.045,
        "Criterion-compatible set",
        linestyle="--",
        weight="bold",
        fontsize=8.4,
    )

    arrow(ax, (0.47, 0.875), (0.255, 0.705), rad=0.03)
    arrow(ax, (0.53, 0.875), (0.745, 0.71), rad=-0.03)
    arrow(ax, (0.165, 0.805), (0.205, 0.705), dashed=True)
    arrow(ax, (0.835, 0.805), (0.805, 0.71), dashed=True)
    arrow(ax, (0.252, 0.625), (0.252, 0.58))
    arrow(ax, (0.748, 0.615), (0.748, 0.575))
    arrow(ax, (0.748, 0.465), (0.748, 0.453))
    arrow(ax, (0.748, 0.405), (0.748, 0.38))

    ax.text(
        0.5,
        0.302,
        "3. Primary-diagnosis selection",
        ha="center",
        va="center",
        fontsize=12.2,
        fontweight="bold",
        color=COLORS["ink"],
    )
    box(
        ax,
        0.18,
        0.195,
        0.235,
        0.075,
        "Direct-Answer (DA)\nKeep the proposed primary",
        face="det",
        linewidth=1.9,
        weight="bold",
        fontsize=8.8,
    )
    box(
        ax,
        0.585,
        0.195,
        0.235,
        0.075,
        "Nominate-then-Select (NtS)\nUse ranking + compatible set",
        face="det",
        linewidth=1.9,
        weight="bold",
        fontsize=8.6,
    )
    box(
        ax,
        0.355,
        0.105,
        0.29,
        0.055,
        "Committed primary diagnosis",
        face="final",
        linewidth=2.2,
        weight="bold",
        fontsize=9.2,
    )

    arrow(ax, (0.235, 0.445), (0.29, 0.27), rad=0.08)
    arrow(ax, (0.35, 0.445), (0.66, 0.27), rad=-0.12)
    arrow(ax, (0.748, 0.335), (0.72, 0.27), rad=0.03)
    arrow(ax, (0.298, 0.195), (0.43, 0.16), rad=-0.05)
    arrow(ax, (0.702, 0.195), (0.57, 0.16), rad=0.05)

    box(
        ax,
        0.08,
        0.015,
        0.84,
        0.055,
        "Records retained for review: ranked candidates  |  criterion states  |  evidence notes  |  missing information  |  compatible set  |  selection result",
        face="missing",
        linestyle=":",
        linewidth=1.8,
        weight="bold",
        fontsize=8.4,
    )

    save(fig, path)


def make_worked_example(path: Path) -> None:
    fig, ax = plt.subplots(figsize=(12.5, 10.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    box(
        ax,
        0.14,
        0.90,
        0.72,
        0.07,
        "Complete constructed transcript\nIllustrative case - not a patient record or exported model trace",
        face="input",
        linewidth=1.8,
        weight="bold",
        fontsize=10,
    )
    box(ax, 0.13, 0.72, 0.24, 0.105, "Diagnosis path\n\nDiagnostician", face="llm", weight="bold", fontsize=9.7)
    box(
        ax,
        0.05,
        0.48,
        0.40,
        0.20,
        "Illustrative ranked candidates\n\n1. F41.1 Generalized anxiety disorder\n2. F32 Depressive episode\n3. F51 Nonorganic sleep disorder\n\nProposed primary: F41.1\nOptional comorbidity: None",
        linestyle="--",
        weight="bold",
        fontsize=8.5,
        align="left",
    )
    ax.text(
        0.25,
        0.455,
        "Up to five candidates may be retained; only the leading three are shown.",
        ha="center",
        va="top",
        fontsize=7.6,
        color=COLORS["muted"],
        style="italic",
    )
    box(
        ax,
        0.63,
        0.71,
        0.26,
        0.115,
        "Criterion-checking path\n\nDiagnosis-specific Criterion Checkers\nAll 14 categories checked",
        face="llm",
        weight="bold",
        fontsize=8.4,
    )
    box(
        ax,
        0.50,
        0.56,
        0.21,
        0.13,
        "F32\n\nCore symptoms: met\nDuration: met\nAssociated symptoms: met\n\nIncluded",
        linestyle="--",
        weight="bold",
        fontsize=7.9,
        align="left",
    )
    box(
        ax,
        0.75,
        0.53,
        0.22,
        0.16,
        "F41.1\n\nMulti-area worry: met\nRequired duration:\ninsufficient_evidence\nAssociated symptoms:\ninsufficient_evidence\n\nNot included",
        linestyle="--",
        weight="bold",
        fontsize=7.4,
        align="left",
    )
    box(
        ax,
        0.61,
        0.39,
        0.26,
        0.10,
        "F31\n\nPrevious manic episode: not_met\n\nNot included",
        linestyle="--",
        weight="bold",
        fontsize=7.9,
        align="left",
    )
    box(ax, 0.64, 0.285, 0.24, 0.065, "Compatibility Auditor", face="det", linewidth=2.0, weight="bold", fontsize=8.8)
    box(ax, 0.67, 0.215, 0.18, 0.045, "Compatible set: {F32}", linestyle="--", weight="bold", fontsize=8.2)
    arrow(ax, (0.43, 0.90), (0.25, 0.825))
    arrow(ax, (0.57, 0.90), (0.76, 0.825))
    arrow(ax, (0.25, 0.72), (0.25, 0.68))
    arrow(ax, (0.76, 0.71), (0.605, 0.69), rad=0.05)
    arrow(ax, (0.76, 0.71), (0.86, 0.69), rad=-0.04)
    arrow(ax, (0.76, 0.71), (0.74, 0.49), rad=0)
    arrow(ax, (0.74, 0.39), (0.76, 0.35))
    arrow(ax, (0.76, 0.285), (0.76, 0.26))
    box(
        ax,
        0.06,
        0.085,
        0.38,
        0.10,
        "Direct-Answer\n\nKeep the proposed primary\nCommitted primary: F41.1",
        face="final",
        linewidth=2.2,
        weight="bold",
        fontsize=9.0,
    )
    box(
        ax,
        0.56,
        0.085,
        0.38,
        0.10,
        "Nominate-then-Select\n\nChoose the highest-ranked compatible candidate\nCommitted primary: F32",
        face="final",
        linewidth=2.2,
        weight="bold",
        fontsize=8.7,
    )
    arrow(ax, (0.25, 0.48), (0.25, 0.185))
    arrow(ax, (0.45, 0.52), (0.67, 0.185), rad=-0.12)
    arrow(ax, (0.76, 0.215), (0.75, 0.185))
    box(
        ax,
        0.20,
        0.012,
        0.60,
        0.05,
        "Important missing information\nOnset and duration of the anxiety symptoms remain unclear",
        face="missing",
        linestyle=":",
        linewidth=2.0,
        weight="bold",
        fontsize=9.0,
    )
    save(fig, path)


def main() -> None:
    if Path("school/main.tex").exists():
        out_dir = Path("figures")
    elif Path("paper/school/HiED_school_version.tex").exists():
        out_dir = Path("paper/figures")
    else:
        raise FileNotFoundError("Could not identify the School thesis repository layout")

    make_hied_two_path_architecture(out_dir / "fig_hied_two_path_architecture.pdf")
    make_worked_example(out_dir / "fig_worked_example_flow.pdf")
    print(f"Generated Chapter 3 figures in {out_dir}")


if __name__ == "__main__":
    main()
