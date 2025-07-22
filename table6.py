import pandas as pd

# Load the CSV file
df = pd.read_csv("all_paper_for_review.csv")  # Replace with your filename

# Ensure the 'Cited by' column is numeric
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)

# Sort by 'Cited by' in descending order
df_sorted = df.sort_values(by="Cited by", ascending=False)

# Select top 10 most cited papers
top_10_cited = df_sorted.head(10)

# Save to new CSV file
top_10_cited.to_csv("top_10_cited_papers.csv", index=False)

print("✅ Top 10 cited papers saved to 'top_10_cited_papers.csv'")
