import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv("all_paper_for_review.csv")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").dropna().astype(int)
# df = df[df["Year"] > 2016]

year_counts = df["Year"].value_counts().sort_index()
cumulative = year_counts.cumsum()

# Plot setup
fig, ax1 = plt.subplots(figsize=(10, 5))

x_vals = year_counts.index.astype(int)

# Bar plot for yearly publications
bars = ax1.bar(
    x_vals,
    year_counts.values,
    color='teal',
    label="Annual Number of Publications"
)

ax1.set_ylabel("Yearly Publications", color='teal')
ax1.set_xlabel("Release Year")
ax1.tick_params(axis='y', labelcolor='teal')
ax1.set_xticks(x_vals)
ax1.set_xticklabels(x_vals)

# Annotate bar values
for x, y in zip(x_vals, year_counts.values):
    ax1.text(x, y, str(y), ha='center', va='bottom', fontsize=9,color="#17becf")

# Line plot for cumulative publications
ax2 = ax1.twinx()
line, = ax2.plot(
    x_vals,
    cumulative.values,
    color="brown",
    marker='o',
    linewidth=2,
    label="Cumulative Publications Count"
)
ax2.set_ylabel("Accumulated Publications", color="brown")
ax2.tick_params(axis='y', labelcolor="brown")

# Annotate cumulative values
for x, y in zip(x_vals, cumulative.values):
    ax2.text(x+0.1, y-1, str(y), ha='left', va='top', fontsize=9,color="brown")

# Combined Legend
lines_labels = [bars, line]
labels = [l.get_label() for l in lines_labels]
legend = ax2.legend(lines_labels, labels, loc='upper left', frameon=False)

legend.get_texts()[0].set_color("teal")     # Bar legend label
legend.get_texts()[1].set_color("brown")    # Line legend label
# Save and show
plt.title("Publication Trends: Yearly and Cumulative")
plt.tight_layout()
plt.savefig("1_bar_line_with_legend_annotated.png", dpi=300)
plt.show()
