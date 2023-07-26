import requests
from bs4 import BeautifulSoup
import time

START_URL = "https://dom.mirkvartir.ru/%D0%A1%D0%B2%D0%B5%D1%80%D0%B4%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C/%D0%97%D0%B0%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/"

def get_houses_links () -> list:
    start_time = time.time()

    houses_links = []
    page = 1
    response = requests.get(START_URL)

    while response.status_code != 404:
        url = f"{START_URL}?p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        links_ResultSet = soup.find_all("a", {"class": "OffersListItem_offerTitle__3GQ_0"})

        for link in links_ResultSet:
            if "Дом" in link.next_element.text:
                houses_links.append(link.attrs["href"])
            else:
                continue
        
        page+=1

    end_time = time.time()
    print(f"Время, затраченное на парсинг ссылок = {str(end_time-start_time)[0:4]}")
                
    return houses_links
