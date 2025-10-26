import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
}

def scrape_movie_details(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Titlu
    title = soup.select_one('h1 span').get_text(strip=True) if soup.select_one('h1 span') else "N/A"

    # Rating IMDb
    rating = "N/A"
    rating_tag = soup.select_one('div[data-testid="hero-rating-bar__aggregate-rating__score"] span')
    if rating_tag:
        rating = rating_tag.get_text(strip=True)

    # Durată
    runtime = "N/A"
    hero_ul = soup.select_one('div.sc-14a487d5-3 ul.ipc-inline-list.ipc-inline-list--show-dividers')
    if hero_ul:
        runtime_li = hero_ul.find_all('li')[-1]
        runtime = runtime_li.get_text(strip=True) if runtime_li else "N/A"

    # Genuri
    genres = [g.get_text(strip=True) for g in soup.select('div.ipc-chip-list__scroller a.ipc-chip span.ipc-chip__text')]
    genres = ', '.join(genres) if genres else "N/A"

    # Director(i), Writers, Stars
    people_section = soup.select('li[data-testid="title-pc-principal-credit"]')
    directors, writers, stars = "N/A", "N/A", "N/A"
    if len(people_section) >= 1:
        directors = ', '.join(a.get_text(strip=True) for a in people_section[0].select('a'))
    if len(people_section) >= 2:
        writers = ', '.join(a.get_text(strip=True) for a in people_section[1].select('a'))
    
    stars = ', '.join([tag.text.strip() for tag in soup.select('a[data-testid="title-cast-item__actor"]')][:10])

    # Popularitate
    popularity = "N/A"
    popularity_div = soup.select_one('div[data-testid="hero-rating-bar__popularity__score"]')
    if popularity_div:
        popularity = popularity_div.get_text(strip=True)

    # Budget
    budget = "N/A"
    budget_tag = soup.select_one('li[data-testid="title-boxoffice-budget"] span.ipc-metadata-list-item__list-content-item')
    if budget_tag:
        budget = budget_tag.get_text(strip=True)

    # Gross worldwide
    gross_worldwide = "N/A"
    gross_tag = soup.select_one('li[data-testid="title-boxoffice-cumulativeworldwidegross"] span.ipc-metadata-list-item__list-content-item')
    if gross_tag:
        gross_worldwide = gross_tag.get_text(strip=True)

    return {
        "Title": title,
        "Rating": rating,
        "Runtime": runtime,
        "Directors": directors,
        "Writers": writers,
        "Stars": stars,
        "Genres": genres,
        "Popularity": popularity,
        "Budget": budget,
        "Gross Worldwide": gross_worldwide,
        "URL": url
    }

def main():
    # Citim link-urile din CSV
    with open("imdb_links.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        movie_links = [row['IMDb Link'] for row in reader]

    print(f"[INFO] Se procesează {len(movie_links)} filme.")

    with open("imdb_movies_data.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Title", "Rating", "Runtime", "Directors", "Writers", "Stars", "Genres", "Popularity", "Budget", "Gross Worldwide", "URL"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, link in enumerate(movie_links):
            print(f"[{i}/{len(movie_links)}] Se procesează: {link}")
            try:
                data = scrape_movie_details(link)
                writer.writerow(data)
            except Exception as e:
                print(f"Eroare la {link}: {e}")
            # time.sleep(0.5)  # mic delay pentru a evita blocarea IMDb

    print("\n Gata! Datele sunt salvate în 'top250_movies.csv'.")

if __name__ == "__main__":
    main()