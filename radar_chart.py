import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# GLOBAL STYLE
# =========================================================
bg_color = '#ffffff'
panel_color = "#faf0e6"

accuracy_color = '#A21942'
macro_color = '#3F7E44'
weighted_color = '#19486A'

text_color = 'black'
grid_color = '#1e293b'

plt.rcParams['font.family'] = 'Roboto'

# =========================================================
# 1. RADAR / SPIDER CHART
# =========================================================

categories = [
    'Accuracy',
    'Macro F1',
    'Weighted F1',
    'Context Understanding',
    'Semantic Learning',
    'Multilingual Support',
    'Scalability'
]

# Random Forest
ml_values = [86.69, 79.00, 86.00, 60, 58, 20, 72]

# DistilBERT
dl_values = [90.24, 85.89, 90.42, 95, 96, 92, 94]

N = len(categories)

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

ml_values += ml_values[:1]
dl_values += dl_values[:1]
angles += angles[:1]

fig = plt.figure(figsize=(10, 10), facecolor=bg_color)

ax = plt.subplot(111, polar=True)
ax.set_facecolor(panel_color)

ax.plot(
    angles,
    ml_values,
    linewidth=3,
    color=accuracy_color,
    label='Random Forest'
)

ax.fill(
    angles,
    ml_values,
    alpha=0.25,
    color=accuracy_color
)

ax.plot(
    angles,
    dl_values,
    linewidth=3,
    color=macro_color,
    label='DistilBERT'
)

ax.fill(
    angles,
    dl_values,
    alpha=0.25,
    color=macro_color
)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(
    categories,
    fontsize=11,
    color='black',
    fontweight='semibold'
)
ax.tick_params(pad=10)

ax.tick_params(axis='y', colors='black')

ax.grid(color=grid_color, linestyle='--', linewidth=1)

legend = ax.legend(
    loc='upper right',
    bbox_to_anchor=(1.25, 1.10),
    fontsize=14,
    frameon=False
)

for text in legend.get_texts():
    text.set_color('black')

plt.tight_layout()

save_path = r"C:\Personal\Projects\SDG_News_classifier\UI\static\images\radar_chart.png"

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches='tight',
    facecolor=fig.get_facecolor()
)

print(f"Radar Chart Saved:\n{save_path}")

plt.show()