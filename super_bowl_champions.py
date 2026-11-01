# Source: https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions
# Prints the Super Bowl game, winning team, losing team, and final score.

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"


def main():
    response = requests.get(URL, headers={"User-Agent": "StudentWebScrapingAssignment/1.0 (learning Python)"}, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    table = None
    for candidate in soup.select("table.wikitable"):
        headers = " ".join(th.get_text(" ", strip=True).lower() for th in candidate.select("tr th"))
        if "winning team" in headers and "losing team" in headers and "venue" in headers:
            table = candidate
            break

    if table is None:
        print("Could not find the Super Bowl results table.")
        return

    print("SUPER BOWL CHAMPIONS")
    print("-" * 85)
    count = 0
    for row in table.select("tr"):
        cells = row.find_all(["th", "td"], recursive=False)
        if len(cells) < 6:
            continue
        game = cells[0].get_text(" ", strip=True)
        winner = cells[2].get_text(" ", strip=True).split("(")[0].strip().removesuffix(" N").removesuffix(" A")
        winner_score = cells[3].get_text(" ", strip=True)
        loser = cells[4].get_text(" ", strip=True).split("(")[0].strip().removesuffix(" N").removesuffix(" A")
        loser_score = cells[5].get_text(" ", strip=True)
        print(f"Super Bowl {game}: {winner} {winner_score} - {loser} {loser_score}")
        count += 1

    print(f"\nTotal games found: {count}")


if __name__ == "__main__":
    main()
