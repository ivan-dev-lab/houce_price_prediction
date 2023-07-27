import requests
from bs4 import BeautifulSoup
import time

START_URL = "https://dom.mirkvartir.ru/%D0%A1%D0%B2%D0%B5%D1%80%D0%B4%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C/%D0%97%D0%B0%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/"

def get_houses_urls () -> list:
    start_time = time.time()

    houses_urls = []
    page = 1
    response = requests.get(START_URL)

    while response.status_code != 404:
        url = f"{START_URL}?p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        urls_ResultSet = soup.find_all("a", {"class": "OffersListItem_offerTitle__3GQ_0"})

        for link in urls_ResultSet:
            if "Дом" in link.next_element.text:
                houses_urls.append(link.attrs["href"])
            else:
                continue
        
        page+=1

    end_time = time.time()
    print(f"Время, затраченное на парсинг ссылок = {str(end_time-start_time)[0:4]} сек.")
                
    return houses_urls

def get_house_parameters (house_url: str) -> dict:
    house_parameters = {
        "price": str, # в руб.
        "area_house": float, # в м2
        "area_land": float, # в сот.
        "type": str, 
        "num_of_floors": int, # в шт.
        "num_of_rooms": int, # в шт.
    }

    response = requests.get(house_url)
    soup = BeautifulSoup(response.text, "lxml")

    house_parameters["price"] = soup.find("div", {"class": "price m-all"}).next_element.text.replace("\u2009", "")

    parent_parameter_div_ResultSet = soup.find_all("div", {"class": "sc-1u2rf9n cktnNC"})
    parameters_list = []

    for child in parent_parameter_div_ResultSet:
        parameters_list.append(child.text)

    house_parameters["area_house"] = float(parameters_list[1].replace("Площадь", "")[0:3])
    house_parameters["area_land"] = float(parameters_list[1].split("участок ")[1][0])
    house_parameters["type"] = parameters_list[3].replace("Тип участка", "")
    house_parameters["num_of_floors"] = int(parameters_list[2].replace("Этажность", "")[0])
    house_parameters["num_of_rooms"] = int(parameters_list[0][-1:])

    return house_parameters

    return houses_links
