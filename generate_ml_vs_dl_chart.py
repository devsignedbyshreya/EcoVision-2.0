import matplotlib.pyplot as plt
import numpy as np

# =========================
# DATA
# =========================
models = [
    'Random\nForest',
    'DistilBERT'
]

accuracy = [86.69, 90.24]
macro_f1 = [79.00, 85.89]
weighted_f1 = [86.00, 90.42]

x = np.array([0, 0.5])
width = 0.15

# =========================
# COLORS
# =========================
bg_color = '#ffffff'
panel_color = '#ffffff'

accuracy_color = '#A21942'
macro_color = '#3F7E44'
weighted_color = '#19486A'

text_color = 'black'
grid_color = '#0f172a'

# =========================
# FIGURE
# =========================
fig, ax = plt.subplots(figsize=(16, 8))

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(panel_color)

# =========================
# BARS
# =========================
bars1 = ax.bar(
    x - width,
    accuracy,
    width,
    color=accuracy_color,
    edgecolor='black',
    linewidth=1.5,
    label='Accuracy (%)'
)

bars2 = ax.bar(
    x,
    macro_f1,
    width,
    color=macro_color,
    edgecolor='black',
    linewidth=1.5,
    label='Macro F1 (%)'
)

bars3 = ax.bar(
    x + width,
    weighted_f1,
    width,
    color=weighted_color,
    edgecolor='black',
    linewidth=1.5,
    label='Weighted F1 (%)'
)

# =========================
# AXES
# =========================
ax.set_xticks(x)

ax.set_xticklabels(
    models,
    fontsize=22,
    color='black',
    weight='bold'
)

ax.set_ylabel(
    'Score (%)',
    fontsize=16,
    color='black',
    weight='bold',
    labelpad=0
)

ax.set_ylim(0, 100)

# =========================
# GRID
# =========================
ax.grid(
    axis='y',
    linestyle='--',
    linewidth=1,
    color=grid_color,
    alpha=0.7
)

ax.set_axisbelow(True)

# =========================
# TICKS
# =========================
ax.tick_params(axis='y', colors='black', labelsize=18)

ax.tick_params(axis='x', pad=10)

# =========================
# SPINES
# =========================
for spine in ax.spines.values():
    spine.set_color('#2B3A5A')
    spine.set_linewidth(2)

# =========================
# LEGEND
# =========================
legend = ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, 1.15),
    ncol=3,
    fontsize=20,
    frameon=False
)

for text in legend.get_texts():
    text.set_color('black')

# =========================
# VALUE LABELS
# =========================
def add_labels(bars):
    for bar in bars:
        h = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 1.2,
            f'{h:.2f}%',
            ha='center',
            va='bottom',
            fontsize=16,
            color='black',
            weight='bold'
        )

add_labels(bars1)
add_labels(bars2)
add_labels(bars3)

# =========================
# LAYOUT FIX
# =========================
plt.subplots_adjust(
    left=0.08,
    right=0.97,
    top=0.82,
    bottom=0.16
)

# =========================
# SAVE
# =========================
save_path = r"C:\Personal\Projects\SDG_News_classifier\UI\static\images\ml_vs_dl_research.png"

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches='tight',
    facecolor=fig.get_facecolor()
)

print(f"Saved to:\n{save_path}")

plt.show()