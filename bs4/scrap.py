import re
import requests
from bs4 import BeautifulSoup

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

url =  "https://pt.wikipedia.org/wiki/Categoria:Her%C3%B3is_da_DC_Comics"
response = requests.get(url, headers=headers)
content = response.text

soup = BeautifulSoup(content, 'html.parser')



div_list = soup.find('div', id="mw-pages")

a_list = div_list.find_all('a')

for a in a_list:
    hero_name = a.get_text()
    link = re.search(r"href=\"(.*)\"", str(a))
    hero = f"Name: {hero_name} - Link = https://pt.wikipedia.org{link.group(0)}\n"

    with open("dc_heros.txt", "a") as file:
        file.write(hero)