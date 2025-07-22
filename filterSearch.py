import subprocess
from pathlib import Path

# Ordered list of directories to run scripts from
folders = [
    "MP_AUV",
    "Plastic_AUV",
    "MP_Detection_Method",
]

# Find related papers with venues filter
for folder in folders:
    script_path = Path(folder) / "Sematic_with_filter.py"
    print(f"\n🚀 Running script in: {folder}")

    while True:
        try:
            subprocess.run(["python", str(script_path)], check=True)
            print(f"✅ Finished: {script_path}")
            break  # Exit the loop if successful
        except subprocess.CalledProcessError as e:
            print(f"❌ Error while running {script_path}: {e}")
            print("🔁 Retrying...")

# Combine all to one table
import pandas as pd
from pathlib import Path

# Step 1: Get all .csv files ending with "sematic.csv"
csv_files = list(Path(".").glob("*filtered_papers_sematic.csv"))

# Step 2: Read and concatenate them
dataframes = [pd.read_csv(f) for f in csv_files]
combined_df = pd.concat(dataframes, ignore_index=True)

# Step 3: Show length before removing duplicates
original_len = len(combined_df)

# Step 4: Remove duplicates based on Title and DOI
deduped_df = combined_df.drop_duplicates(subset=["Title", "DOI"])

# Step 5: Show length after removing duplicates
deduped_len = len(deduped_df)

# Step 6: Save to new CSV
output_path = Path("combined_deduplicated_paper.csv")
deduped_df.to_csv(output_path, index=False)

# Step 7: Print result
print(f"📊 Combined total before deduplication: {original_len}")
print(f"✅ After deduplication: {deduped_len}")
print(f"💾 Saved to: {output_path.resolve()}")


# filter out cited by > 5

# Load the original CSV
df = pd.read_csv("combined_deduplicated_paper.csv")

# Filter rows where the "test" column > 1
df = df[df["Cited by"] > 5]
# Sort by "test" column in descending order
df = df.sort_values(by="Cited by", ascending=False)

filtered_df = df[df["Foldername"] == "MDM_WF"]
print(" filtered_df length:",len(filtered_df))
# Save the filtered result to a new CSV
filtered_df.to_csv("filtered_output.csv", index=False)

