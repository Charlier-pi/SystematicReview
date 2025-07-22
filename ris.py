import csv
from pathlib import Path

# === CONFIGURATION ===
csv_file_path = "all_paper_for_review.csv"  # 🔁 Replace with your actual CSV file
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
