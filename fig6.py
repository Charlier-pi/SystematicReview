import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("all_paper_for_review.csv")  # Replace with actual file path
df["Source title"] = df["Source title"].fillna("Unknown").astype(str).str.strip()
macaron_colors = [
    "#FFF2D7","#D3C5E5","#66A5AD","#6AB187","#EDF4F2","#FFBB00","#D09683","#bae1ff",
]
# Count publications per journal
source_counts = df["Source title"].value_counts()
major_sources = source_counts[source_counts > 2]
minor_count = source_counts[source_counts <= 2].sum()

# Combine major sources and "Others"
final_counts = major_sources.copy()
final_counts["Others"] = minor_count

# Custom function to return the count instead of percentage
def count_autopct(pct, all_vals):
    absolute = int(round(pct/100. * sum(all_vals)))
    return f"{absolute}"

# Plot
fig, ax = plt.subplots(figsize=(8, 8))
colors = plt.cm.tab20.colors
wedges, texts, autotexts = ax.pie(
    final_counts.values,
    autopct=lambda pct: count_autopct(pct, final_counts.values),
    startangle=140,
    colors=macaron_colors,
    wedgeprops={'edgecolor': 'white'},
    pctdistance=0.7
)

# Add legend for source titles
ax.legend(wedges, final_counts.index, title="Publication Source", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)


# Style count labels
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(12)

# Title
plt.title("Publication Counts by Publication Source", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
