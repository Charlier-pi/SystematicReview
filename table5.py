import pandas as pd

# Load CSV
df = pd.read_csv("all_paper_for_review.csv")  # Replace with your actual file name
df["Source title"] = df["Source title"].fillna("Unknown").astype(str).str.strip()
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(0).astype(int)

# Group by source title: total citations and publication year range
citation_stats = df.groupby("Source title").agg({
    "Cited by": "sum",
    "Year": ["min", "max"]
}).reset_index()

# Flatten MultiIndex columns
citation_stats.columns = ["Source title", "Total Citations", "Year Start", "Year End"]

# Get Top 10 by total citations
top10 = citation_stats.sort_values(by="Total Citations", ascending=False).head(11)

# Save to CSV
top10.to_csv("top10_cited_journals.csv", index=False)

print("✅ Saved top 10 cited journals to 'top10_cited_journals.csv'")
