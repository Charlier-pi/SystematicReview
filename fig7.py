import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("all_paper_for_review.csv")  # Replace with your file name
df["Source title"] = df["Source title"].fillna("Unknown").astype(str).str.strip()
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)

# Macaron color palette
macaron_colors = [
    "#FFF2D7", "#D3C5E5", "#66A5AD", "#6AB187",
    "#EDF4F2", "#FFBB00", "#D09683", "#bae1ff"
]

# Group by journal to get publication count and citation sum
source_pub_counts = df["Source title"].value_counts()
source_citations = df.groupby("Source title")["Cited by"].sum()

# Split major/minor journals
major_sources = source_pub_counts[source_citations > 200]
minor_sources = source_pub_counts[source_citations <= 200]

# Build citation dataset for major journals
major_citations = source_citations[major_sources.index]

# Calculate total citations for "Others"
minor_citation_total = source_citations[minor_sources.index].sum()

# Combine into final citation data for pie chart
final_citations = major_citations.copy()
final_citations["Others"] = minor_citation_total

# Sort pie slices by citation count (descending)
final_citations = final_citations.sort_values(ascending=False)

# Function to display actual counts on pie
def count_autopct(pct, all_vals):
    absolute = int(round(pct/100. * sum(all_vals)))
    return f"{absolute}"

# Pie chart
fig, ax = plt.subplots(figsize=(8, 8))
colors = plt.cm.tab20.colors
wedges, texts, autotexts = ax.pie(
    final_citations.values,
    autopct=lambda pct: count_autopct(pct, final_citations.values),
    startangle=0,
    colors=macaron_colors,
    wedgeprops={'edgecolor': 'white'},
    pctdistance=0.85
)

# Add legend for source titles
ax.legend(wedges, final_citations.index, title="Publication Source", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)

# Style count labels
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(12)

# Title
plt.title("Cumulative Citations by Publication Source", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
