import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# GLOBAL STYLE
# =========================================================
bg_color = '#ffffff'
panel_color = "#ffffff"

accuracy_color = '#A21942'
macro_color = '#3F7E44'
weighted_color = '#19486A'

text_color = 'black'
grid_color = '#1e293b'

plt.rcParams['font.family'] = 'Roboto'

# =========================================================
# 2. TRAINING LOSS CURVE
# =========================================================

epochs = [1, 2, 3, 4]

training_loss = [0.454217, 0.335166, 0.308578, 0.196765]
validation_loss = [0.568146, 0.536893, 0.608805, 0.609376]

fig, ax = plt.subplots(figsize=(12, 7))

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(panel_color)

ax.plot(
    epochs,
    training_loss,
    marker='o',
    linewidth=3,
    markersize=10,
    color=accuracy_color,
    label='Training Loss'
)

ax.plot(
    epochs,
    validation_loss,
    marker='o',
    linewidth=3,
    markersize=10,
    color=macro_color,
    label='Validation Loss'
)

ax.set_xlabel(
    'Epochs',
    fontsize=18,
    color='black',
    weight='bold',
    labelpad=15
)

ax.set_ylabel(
    'Loss',
    fontsize=18,
    color='black',
    weight='bold',
    labelpad=15
)

ax.tick_params(colors='black', labelsize=14)

ax.grid(
    linestyle='--',
    linewidth=1,
    color=grid_color,
    alpha=0.7
)

for spine in ax.spines.values():
    spine.set_color('#2B3A5A')
    spine.set_linewidth(2)

legend = ax.legend(
    fontsize=14,
    frameon=False
)

for text in legend.get_texts():
    text.set_color('black')

plt.tight_layout()

save_path = r"C:\Personal\Projects\SDG_News_classifier\UI\static\images\training_loss_curve.png"

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches='tight',
    facecolor=fig.get_facecolor()
)

print(f"Training Loss Curve Saved:\n{save_path}")

plt.show()

# =========================================================
# 3. ACCURACY / F1 IMPROVEMENT CURVE
# =========================================================

accuracy = [80.59, 88.97, 89.12, 89.09]
macro_f1 = [79.01, 83.78, 83.96, 84.60]
weighted_f1 = [81.89, 89.16, 89.25, 89.30]

fig, ax = plt.subplots(figsize=(12, 7))

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(panel_color)

ax.plot(
    epochs,
    accuracy,
    marker='o',
    linewidth=3,
    markersize=10,
    color=accuracy_color,
    label='Accuracy'
)

ax.plot(
    epochs,
    macro_f1,
    marker='o',
    linewidth=3,
    markersize=10,
    color=macro_color,
    label='Macro F1'
)

ax.plot(
    epochs,
    weighted_f1,
    marker='o',
    linewidth=3,
    markersize=10,
    color=weighted_color,
    label='Weighted F1'
)

ax.set_xlabel(
    'Epochs',
    fontsize=18,
    color='black',
    weight='bold',
    labelpad=15
)

ax.set_ylabel(
    'Performance (%)',
    fontsize=18,
    color='black',
    weight='bold',
    labelpad=15
)

ax.set_ylim(70, 95)

ax.tick_params(colors='black', labelsize=14)

ax.grid(
    linestyle='--',
    linewidth=1,
    color=grid_color,
    alpha=0.7
)

for spine in ax.spines.values():
    spine.set_color('#2B3A5A')
    spine.set_linewidth(2)

legend = ax.legend(
    fontsize=14,
    frameon=False
)

for text in legend.get_texts():
    text.set_color('black')

plt.tight_layout()

save_path = r"C:\Personal\Projects\SDG_News_classifier\UI\static\images\accuracy_f1_curve.png"

plt.savefig(
    save_path,
    dpi=300,
    bbox_inches='tight',
    facecolor=fig.get_facecolor()
)

print(f"Accuracy/F1 Curve Saved:\n{save_path}")

plt.show()