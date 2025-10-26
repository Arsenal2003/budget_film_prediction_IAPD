import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.imdb.com"
TOP_250_URL = f"{BASE_URL}/search/title/?groups=top_1000&count=100&sort=user_rating,desc"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
}

def get_movie_links():
    response = requests.get(TOP_250_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for a in soup.select("li.ipc-metadata-list-summary-item a.ipc-title-link-wrapper"):
        href = a.get('href')
        if href and '/title/' in href:
            links.append(BASE_URL + href.split('?')[0])
    return list(set(links))  # elimină duplicatele

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
    # Selectăm lista de sub titlu (hero section)
    hero_ul = soup.select_one('div.sc-14a487d5-3 ul.ipc-inline-list.ipc-inline-list--show-dividers')
    if hero_ul:
        # ultimul <li> din această listă este durata
        runtime_li = hero_ul.find_all('li')[-1]
        runtime = runtime_li.get_text(strip=True) if runtime_li else "N/A"

    # Genuri (update pentru noua structură)
    genres = [g.get_text(strip=True) for g in soup.select('div.ipc-chip-list__scroller a.ipc-chip span.ipc-chip__text')]
    genres = ', '.join(genres) if genres else "N/A"

    # Director(i), Writers, Stars
    people_section = soup.select('li[data-testid="title-pc-principal-credit"]')
    directors, writers, stars = "N/A", "N/A", "N/A"

    if len(people_section) >= 1:
        directors = ', '.join(a.get_text(strip=True) for a in people_section[0].select('a'))
    if len(people_section) >= 2:
        writers = ', '.join(a.get_text(strip=True) for a in people_section[1].select('a'))
    if len(people_section) >= 3:
        stars = ', '.join(a.get_text(strip=True) for a in people_section[2].select('a'))

    # Top/Popularitate
    popularity = "N/A"
    popularity_div = soup.select_one('div[data-testid="hero-rating-bar__popularity__score"]')
    if popularity_div:
        popularity = popularity_div.get_text(strip=True)

    return {
        "Title": title,
        "Rating": rating,
        "Runtime": runtime,
        "Directors": directors,
        "Writers": writers,
        "Stars": stars,
        "Genres": genres,
        "Popularity": popularity,
        "URL": url
    }

def main():
    movie_links = get_movie_links()
    print(f"[INFO] Am găsit {len(movie_links)} filme.")
    
    with open("top250_movies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Rating", "Runtime", "Directors", "Writers", "Stars", "Genres", "Popularity", "URL"])
        writer.writeheader()

        for i, link in enumerate(movie_links, 1):
            print(f"[{i}/{len(movie_links)}] Se procesează: {link}")
            try:
                data = scrape_movie_details(link)
                writer.writerow(data)
            except Exception as e:
                print(f"Eroare la {link}: {e}")
            time.sleep(1)  # mic delay pentru a evita blocarea de la IMDb

    print("\n✅ Gata! Datele sunt salvate în 'top250_movies.csv'.")

if __name__ == "__main__":
    main()
