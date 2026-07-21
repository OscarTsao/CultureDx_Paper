from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})

labels = ["F20", "F31", "F32", "F39", "F41", "F42", "F43", "F45", "F51", "F98", "Z71", "Others"]
M = np.array([
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 7, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 326, 3, 24, 4, 0, 0, 1, 0, 0, 0],
    [3, 1, 43, 3, 8, 1, 0, 0, 0, 1, 0, 0],
    [2, 0, 178, 8, 159, 10, 0, 0, 1, 0, 0, 0],
    [1, 0, 2, 0, 6, 16, 0, 0, 0, 0, 0, 0],
    [0, 0, 10, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 20, 1, 13, 0, 1, 0, 0, 1, 0, 0],
    [2, 0, 18, 3, 6, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 7, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [12, 0, 37, 4, 26, 4, 0, 0, 0, 2, 0, 0],
], dtype=float)

fig, ax = plt.subplots(figsize=(7.2, 6.1), constrained_layout=True)
mesh = ax.pcolormesh(
    np.arange(M.shape[1] + 1),
    np.arange(M.shape[0] + 1),
    M,
    cmap="Blues",
    vmin=0,
    vmax=M.max(),
    edgecolors="white",
    linewidth=0.55,
    shading="flat",
)
ax.set_xlim(0, M.shape[1])
ax.set_ylim(M.shape[0], 0)
ax.set_aspect("equal")
ax.set_xticks(np.arange(len(labels)) + 0.5, labels=labels, rotation=48, ha="right")
ax.set_yticks(np.arange(len(labels)) + 0.5, labels=labels)
ax.set_xlabel("Predicted parent")
ax.set_ylabel("Benchmark gold parent")
ax.tick_params(length=0)

threshold = M.max() * 0.42
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        value = int(M[i, j])
        if value:
            ax.text(
                j + 0.5,
                i + 0.5,
                str(value),
                ha="center",
                va="center",
                fontsize=8.5,
                color="white" if value >= threshold else "#1f2933",
            )

cbar = fig.colorbar(mesh, ax=ax, fraction=0.048, pad=0.04)
cbar.set_label("Cases")
cbar.outline.set_linewidth(0.8)

out_dir = Path(__file__).resolve().parent.parent
fig.savefig(out_dir / "fig_d_confusion_heatmap.pdf", bbox_inches="tight")
fig.savefig(Path(__file__).with_suffix(".svg"), bbox_inches="tight")
plt.close(fig)
