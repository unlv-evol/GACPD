import requests
from bs4 import BeautifulSoup
import csv
import sys
import time
import os

confs = ["chi", "icse"]
years = []
years.extend([str(year) for year in range(2024, 1999, -1)])  # 2024 -> 2000
filtering = False
for conf in confs:
    folder = conf+"-full"
    for year in years:
        # URL to scrape
        url = f"https://dblp.org/db/conf/{conf}/{conf}{year}.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Keywords to filter
        keywords = [" merge ", " merges ", "merge conflict", "merge", "conflict", "conflicts"]

        # Extract paper titles and first authors
        papers = []
        for entry in soup.find_all("cite", class_="data"):
            title = entry.find("span", class_="title").text.strip()
            # Check if any keyword is in the title (case-insensitive)
            if filtering is True:
                if any(keyword.lower() in title.lower() for keyword in keywords):
                    authors = entry.find_all("span", itemprop="author")
                    first_author = authors[0].text.strip() if authors else "N/A"
                    papers.append([title, first_author, f"{conf.upper()}", year, 0, 0, 0, 0])
            else:
                authors = entry.find_all("span", itemprop="author")
                first_author = authors[0].text.strip() if authors else "N/A"
                papers.append([title, first_author, f"{conf.upper()}", year, 0, 0, 0, 0])

        # Save to CSV
        if not os.path.exists(f"{folder}"):
            os.makedirs(f"{folder}", 777)

        csv_filename = f"{folder}/{conf}_{year}_papers.csv"
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Paper Name", "First Author", "Conference", "Year", "Relevant", "Math", "Empirical", "Read"])
            writer.writerows(papers)

        print(f"Data successfully saved to {csv_filename}")
        time.sleep(10)