from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def make_figure(output_path: Path) -> None:
    metrics = ["Committed\nTop-1", "Genuine\nTop-3", "Gold in\ncompatible set"]
    internal = [0.518, 0.802, 0.937]
    external = [0.601, 0.896, 0.786]

    x = np.arange(len(metrics))
    width = 0.34
    fig, ax = plt.subplots(figsize=(9.2, 4.9))

    bars_internal = ax.bar(
        x - width / 2,
        internal,
        width,
        label="LingxiDiag internal",
        color="#B8C6D1",
        edgecolor="#222222",
        hatch="///",
        linewidth=1.1,
    )
    bars_external = ax.bar(
        x + width / 2,
        external,
        width,
        label="MDD-5k external",
        color="#E3B878",
        edgecolor="#222222",
        hatch="...",
        linewidth=1.1,
    )

    ax.set_ylim(0.0, 1.05)
    ax.set_ylabel("Agreement / inclusion rate")
    ax.set_xticks(x, metrics)
    ax.grid(axis="y", alpha=0.25, linewidth=0.7)
    ax.set_axisbelow(True)

    for bars in (bars_internal, bars_external):
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.018,
                f"{bar.get_height():.3f}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)
    ax.text(
        0.5,
        -0.20,
        "Internal denominators: N=1,000 for Top-1/Top-3 and N=915 for compatibility; external N=878.",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8.7,
        color="#444444",
    )

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    fig.subplots_adjust(bottom=0.26, top=0.82, left=0.10, right=0.98)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_path,
        bbox_inches="tight",
        metadata={"CreationDate": None, "ModDate": None},
    )
    plt.close(fig)


def main() -> None:
    root = Path.cwd()
    if (root / "school" / "main.tex").exists():
        output = root / "figures" / "fig_internal_external_gap.pdf"
    elif (root / "paper" / "school" / "HiED_school_version.tex").exists():
        output = root / "paper" / "figures" / "fig_internal_external_gap.pdf"
    else:
        raise FileNotFoundError("Could not identify the School thesis repository layout")

    make_figure(output)
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
