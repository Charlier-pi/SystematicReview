import os
import csv
import requests
from dotenv import load_dotenv
from pathlib import Path
import ast
from keybert import KeyBERT

def search_semantic_scholar_by_venue(query: str,venues: list, max_results):
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SEMANTIC_SCHOLAR_API_KEY")

    headers = {"x-api-key": api_key}
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/search"

    # Parse keyword list from environment variable
    keywords_raw = os.getenv("KEYWORDS_SEMATIC_MDM")
    try:
        keywords = ast.literal_eval(keywords_raw)
        if not isinstance(keywords, list):
            raise ValueError("Parsed keywords is not a list")
        keywords = [k.strip().lower() for k in keywords]
    except Exception as e:
        print(f"⚠️ Failed to parse keywords: {e}")
        keywords = []

    results = []
    limit = 100
    for offset in range(0, max_results, limit):
        params = {
            "query": query,
            "fields": "title,abstract,citationCount,referenceCount,venue,authors,year,externalIds,url,openAccessPdf",
            "limit": min(limit, max_results - offset),
            "offset": offset
        }

        print(f"🔍 Requesting records {offset + 1} to {offset + limit}...")
        response = requests.get(endpoint, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        data = response.json().get("data", [])

        if not data:
            print("✅ No more results.")
            break

        for p in data:
            venue = p.get("venue", "").lower()
            text = f"{p.get('title', '')} {p.get('abstract', '')}".lower()
            if all(k in text for k in keywords):
                if any(v.lower() in venue for v in venues):
                    results.append(p)

    return results

def save_all_papers_to_csv(papers):
    base_path = Path(os.getenv("PATHX"))
    print("base_path",base_path)

    # Build output filename based on keywords
    keywords_raw = os.getenv("KEYWORDS_SEMATIC_MDM", "results").replace(",", "_").replace(" ", "_")
    output_csv = base_path / f"{keywords_raw}_filtered_papers_sematic.csv"

    output_data = []

    for p in papers:
        title = p.get("title", "")
        authors = "; ".join(a["name"] for a in p.get("authors", []))
        citationCount = p.get("citationCount", "")
        venue = p.get("venue", "")
        year = p.get("year", "")
        url = p.get("url", "")
        doi = p.get("externalIds", {}).get("DOI", "")
        pdf_url = p.get("openAccessPdf", {}).get("url", "")
        abstract = p.get("abstract", "")

        if abstract:
            kw_model = KeyBERT()
            kw_tuples = kw_model.extract_keywords(abstract, top_n=5)
            keywords = [item[0] for item in kw_tuples]
        else:
            keywords = []

        row = {
            "Title": title,
            "Authors": authors,
            "Keywords": keywords,
            "Cited by": citationCount,
            "Source title": venue,
            "Year": year,
            "DOI": doi,
            "URL": url,
            "PDF_URL": pdf_url,
            "Abstract": abstract,
        }

        output_data.append(row)

    if output_data:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=output_data[0].keys())
            writer.writeheader()
            writer.writerows(output_data)

        print(f"✅ Saved {len(output_data)} papers to CSV: {output_csv}")
    else:
        print("🚫 No data to save.")

# === Example usage ===
if __name__ == "__main__":
    load_dotenv()
    keyword = os.getenv("KEYWORDS_SEMATIC_MDM")
    print("🔑 Keyword filter:", keyword)


    papers = search_semantic_scholar_by_venue(
        query=keyword,
        max_results=1000,
         venues=[
            "IEEE", "ieee/oes autonomous underwater vehicles", "ieee journal of oceanic engineering",
            "Nature", "Nature Communications", "science", "ieee transactions on neural networks and learning systems",
            "ieee access", "ieee sensors journal", "ieee internet of things journal",
            "international journal of intelligent robotics and applications", "drones", "marine pollution bulletin"
        ]
    )
    print(f"📄 Total matching papers: {len(papers)}")

    save_all_papers_to_csv(papers)
