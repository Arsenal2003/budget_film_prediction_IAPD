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

title = soup.find("h1").text.strip()
rating = soup.find("span", attrs={"class": "sc-bde20123-1 cMEQkK"}).text.strip() if soup.find("span", attrs={"class": "sc-bde20123-1 cMEQkK"}) else None

# Budget and Box Office
box_office_section = soup.find_all("li", attrs={"data-testid": "title-boxoffice-budget"})
budget = box_office_section[0].find("div", class_="ipc-metadata-list-item__content-container").text if box_office_section else "N/A"

gross_section = soup.find_all("li", attrs={"data-testid": "title-boxoffice-cumulativeworldwidegross"})
gross = gross_section[0].find("div", class_="ipc-metadata-list-item__content-container").text if gross_section else "N/A"

# Cast (first 5 actors)
cast_list = []
for tag in soup.select('a[data-testid="title-cast-item__actor"]'):
    cast_list.append(tag.text.strip())
    
    
print("🎬 Title:", title)
print("⭐ Rating:", rating)
print("💵 Budget:", budget)
print("🌍 Gross:", gross)
print("👥 Cast:", cast_list)