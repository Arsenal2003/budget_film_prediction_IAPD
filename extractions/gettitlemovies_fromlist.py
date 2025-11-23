import requests
from bs4 import BeautifulSoup
import time
import csv
import os

def extract_imdb_list(list_url, output_file="imdb_titles.csv"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/128.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.imdb.com/",
    }

    # Ensure URL has trailing slash
    if not list_url.endswith("/"):
        list_url += "/"

    # Initialize CSV if needed
    if not os.path.exists(output_file):
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Link"])

    all_links = set()
    page = 1

    while True:
        url = f"{list_url}?mode=detail&page={page}"
        print(f"\nFetching page {page}: {url}")

        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            print("Page not found (404) — stopping.")
            break
        elif response.status_code != 200:
            print(f"HTTP {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".lister-item, .ipc-metadata-list-summary-item")

        if not items:
            print("No more movies found.")
            break

        new_movies = []
        for item in items:
            a_tag = item.select_one("a[href^='/title/tt']")
            if a_tag:
                title = a_tag.get_text(strip=True)
                href = a_tag["href"].split("?")[0]
                full_link = f"https://www.imdb.com{href}"
                if full_link not in all_links:
                    all_links.add(full_link)
                    new_movies.append((title, full_link))

        # Append to CSV
        if new_movies:
            with open(output_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(new_movies)
            print(f"Page {page}: Added {len(new_movies)} titles (Total: {len(all_links)})")
        else:
            print("ℹNo new titles this page — stopping.")
            break

        page += 1
        time.sleep(1)

    print(f"\nDone! {len(all_links)} total titles saved to '{output_file}'.")


if __name__ == "__main__":
    imdb_list_url = "https://www.imdb.com/list/ls063676660/?view=compact"
    extract_imdb_list(imdb_list_url)
