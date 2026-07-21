from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})

groups = [
    "Committed-primary\nagreement\n(N = 518)",
    "Top-3 candidate\nmiss\n(N = 113)",
    "Ranked but absent from\ncriterion-compatible set\n(N = 12)",
    "Ranked and compatible,\nbut not selected\n(N = 272)",
]
values = np.array([
    [49.0, 23.7, 27.3],
    [48.2, 22.8, 28.9],
    [38.8, 28.5, 32.7],
    [49.9, 23.0, 27.1],
])
colors = ["#59a14f", "#777777", "#f28e2b"]
legend_labels = ["met", "not met", "insufficient evidence"]

fig, ax = plt.subplots(figsize=(8.0, 3.9), constrained_layout=True)
y = np.arange(len(groups))
left = np.zeros(len(groups))
for idx, (label, color) in enumerate(zip(legend_labels, colors)):
    bars = ax.barh(y, values[:, idx], left=left, color=color, edgecolor="white", linewidth=0.8, label=label)
    for row, bar in enumerate(bars):
        width = values[row, idx]
        ax.text(left[row] + width / 2, bar.get_y() + bar.get_height() / 2, f"{width:.1f}%",
                ha="center", va="center", color="white", fontsize=9)
    left += values[:, idx]

ax.set_yticks(y, groups)
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xlabel("Mean within-case share of criterion states (%)")
ax.grid(axis="x", alpha=0.25)
ax.set_axisbelow(True)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), ncol=3, frameon=False, fontsize=10)

out_dir = Path(__file__).resolve().parent.parent
fig.savefig(out_dir / "fig_ch8_criterion_state_composition.pdf", bbox_inches="tight")
fig.savefig(Path(__file__).with_suffix(".svg"), bbox_inches="tight")
plt.close(fig)
