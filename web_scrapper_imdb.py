import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/title/tt4154796/"  # Avengers: Endgame

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.1 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
print(response.status_code)  # Should be 200

# Title
title = soup.find("h1").text.strip() if soup.find("h1") else "N/A"

# Rating (more stable selector)
rating_tag = soup.find("div", attrs={"data-testid": "hero-rating-bar__aggregate-rating__score"})
rating = rating_tag.find("span").text.strip() if rating_tag and rating_tag.find("span") else "N/A"

# Runtime
runtime_tag = soup.find("li", attrs={"data-testid": "title-techspec_runtime"})
runtime = runtime_tag.find("div", class_="ipc-metadata-list-item__content-container").text.strip() if runtime_tag else "N/A"

# Directors
directors_section = soup.find_all("li", attrs={"data-testid": "title-pc-principal-credit"})
directors = [a.text.strip() for a in directors_section[0].select('a[href*="/name/"]')] if len(directors_section) > 0 else []

# Writers
writers = [a.text.strip() for a in directors_section[1].select('a[href*="/name/"]')] if len(directors_section) > 1 else []

# Stars
stars = [a.text.strip() for a in directors_section[2].select('a[href*="/name/"]')] if len(directors_section) > 2 else []

# Genres (fixed selector)
genres = [g.text.strip() for g in soup.select('div[data-testid="genres"] a')] if soup.select('div[data-testid="genres"] a') else []

# Budget and Box Office
budget_tag = soup.find("li", attrs={"data-testid": "title-boxoffice-budget"})
budget = budget_tag.find("div", class_="ipc-metadata-list-item__content-container").text.strip() if budget_tag else "N/A"

gross_tag = soup.find("li", attrs={"data-testid": "title-boxoffice-cumulativeworldwidegross"})
gross = gross_tag.find("div", class_="ipc-metadata-list-item__content-container").text.strip() if gross_tag else "N/A"

# Cast (first 5 actors)
cast = [tag.text.strip() for tag in soup.select('a[data-testid="title-cast-item__actor"]')][:5]

# Print all extracted info
print("\n🎬 Title:", title)
print("⭐ Rating:", rating)
print("⏱️ Runtime:", runtime)
print("🎥 Directors:", directors)
print("✍️ Writers:", writers)
print("🌟 Stars:", stars)
print("🎭 Genres:", genres)
print("💵 Budget:", budget)
print("🌍 Gross:", gross)
print("👥 Cast:", cast)

# Dictionary form
movie_data = {
    "Title": title,
    "Rating": rating,
    "Runtime": runtime,
    "Directors": directors,
    "Writers": writers,
    "Stars": stars,
    "Genres": genres,
    "Budget": budget,
    "Gross": gross,
    "Cast": cast,
}

print("\n✅ Movie data extracted successfully!")
print(movie_data)
