# Source: https://en.wikipedia.org/wiki/List_of_World_Series_champions
# Prints the year, World Series champion, runner-up, and series result.

import re
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_World_Series_champions"


def main():
    response = requests.get(URL, headers={"User-Agent": "StudentWebScrapingAssignment/1.0 (learning Python)"}, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    table = None
    for candidate in soup.select("table.wikitable"):
        headers = " ".join(th.get_text(" ", strip=True).lower() for th in candidate.select("tr th"))
        if "winning team" in headers and "losing team" in headers and "manager" in headers:
            table = candidate
            break

    if table is None:
        print("Could not find the World Series results table.")
        return

    print("WORLD SERIES CHAMPIONS")
    print("-" * 85)
    count = 0
    for row in table.select("tr"):
        cells = row.find_all(["th", "td"], recursive=False)
        if len(cells) < 4:
            continue
        year = cells[0].get_text(" ", strip=True)
        if not re.match(r"^\d{4}", year):
            continue
        if int(year[:4]) > 2025:
            continue
        score_index = next(
            (i for i, cell in enumerate(cells)
             if re.search(r"\d+[–-]\d+", cell.get_text(" ", strip=True))
             and i >= 2), None
        )
        if score_index is None or score_index + 1 >= len(cells):
            continue  # Skip years when no World Series was played.
        winner = re.sub(r"\s*\[[^\]]+\]", "", cells[1].get_text(" ", strip=True).split("(")[0]).strip()
        score = cells[score_index].get_text(" ", strip=True)
        loser = re.sub(r"\s*\[[^\]]+\]", "", cells[score_index + 1].get_text(" ", strip=True).split("(")[0]).strip()
        print(f"{year}: {winner} defeated {loser} (Series: {score})")
        count += 1

    print(f"\nTotal results found: {count}")


if __name__ == "__main__":
    main()
