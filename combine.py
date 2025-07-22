import subprocess
from pathlib import Path

# Ordered list of directories to run scripts from
folders = [
    "MP_AUV",
    "Plastic_AUV",
    "MP_Detection_Method",
]

# Find all related papers
for folder in folders:
    script_path = Path(folder) / "Sematic_without_filter.py"
    print(f"\n🚀 Running script in: {folder}")

    while True:
        try:
            subprocess.run(["python", str(script_path)], check=True)
            print(f"✅ Finished: {script_path}")
            break  # Exit the loop if successful
        except subprocess.CalledProcessError as e:
            print(f"❌ Error while running {script_path}: {e}")
            print("🔁 Retrying...")

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


# generate ris
import csv
from pathlib import Path

# === CONFIGURATION ===
csv_file_path = "filtered_output.csv"  # 🔁 Replace with your actual CSV file
output_dir = Path("ris_from_csv")
output_dir.mkdir(exist_ok=True)

# === READ CSV AND WRITE RIS FILES ===
with open(csv_file_path, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        title = row.get("Title", "").strip()
        authors = row.get("Authors", "").strip()
        abstract = row.get("Abstract", "").strip()
        venue = row.get("Source title", "").strip()
        year = str(row.get("Year", "")).split(".")[0]  # Remove decimal if present
        doi = row.get("DOI", "").strip()
        url = row.get("URL", "").strip()
        keywords = row.get("Keywords", "").strip()

        # Sanitize file name
        safe_filename = "".join(c if c.isalnum() else "_" for c in title)[:100] + ".ris"
        ris_path = output_dir / safe_filename

        # === Write RIS file ===
        with open(ris_path, "w", encoding="utf-8") as ris_file:
            ris_file.write("TY  - JOUR\n")
            
            # Authors (each on its own AU line)
            if authors:
                for author in authors.split(";"):
                    author = author.strip()
                    if author:
                        ris_file.write(f"AU  - {author}\n")
            
            if title:
                ris_file.write(f"TI  - {title}\n")
            if abstract:
                ris_file.write(f"AB  - {abstract}\n")
            if venue:
                ris_file.write(f"JO  - {venue}\n")
            if year:
                ris_file.write(f"PY  - {year}\n")
            if doi:
                ris_file.write(f"DO  - {doi}\n")
            if url:
                ris_file.write(f"UR  - {url}\n")

            # Keywords (each on its own KW line)
            if keywords:
                # print("keywords:",keywords)
                for kw in keywords.split(","):
                #     print("kw1:",kw)
                    kw = kw.strip("[]").replace("'", "").strip()
                #     print("kw2:",kw)
                    if kw:
                        ris_file.write(f"KW  - {kw}\n")
            
            ris_file.write("ER  - \n")

print(f"✅ RIS files saved to: {output_dir.resolve()}")


# plot figure 5

 

