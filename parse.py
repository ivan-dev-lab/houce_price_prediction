import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

START_URL = "https://dom.mirkvartir.ru/%D0%A1%D0%B2%D0%B5%D1%80%D0%B4%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C/%D0%97%D0%B0%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/"

def get_houses_urls () -> list:
    print("Началась работа функции [ get_houses_urls ]\n")
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

        print(f"Количество ссылок в массиве = {len(houses_urls)}")
        page+=1

    print("\nПолучен код 404")

    end_time = time.time()
    print(f"Работа функции составила {str(end_time-start_time)[0:4]} сек.\n")
                
    return houses_urls

def get_house_parameters (house_url: str) -> dict:
    house_parameters = {
        "price": "", # в руб.
        "area_house": 0.0, # в м2
        "area_land": 0.0, # в сот.
        "type": "", 
        "house_material": "",
        "num_of_floors": 0, # в шт.
    }

    response = requests.get(house_url)
    soup = BeautifulSoup(response.text, "lxml")

    house_parameters["price"] = soup.find("div", {"class": "price m-all"}).next_element.text.replace("\u2009", "")

    parent_parameter_div_ResultSet = soup.find_all("div", {"class": "sc-1u2rf9n cktnNC"})
    parameters_list = []

    for child in parent_parameter_div_ResultSet:
        parameters_list.append(child.text)

    if len(parameters_list) >= 4:
        for parameter in parameters_list:
            if parameter.find("Площадь") != -1:
                house_parameters["area_house"] = float(parameter.replace("Площадь", "")[0:3])
                if parameter.find("участок") != -1:
                    house_parameters["area_land"] = float(parameter.split("участок ")[1][:-6])
            elif parameter.find("Тип участка") != -1:
                house_parameters["type"] = parameter.replace("Тип участка", "")
            elif parameter.find("Дом") != -1:
                house_parameters["house_material"] = parameter.replace("Дом", "")
            elif parameter.find("Этажность") != -1:
                house_parameters["num_of_floors"] = int(parameter.replace("Этажность", "")[0])

        for value in house_parameters.values():
            if value == "" or value == 0.0 or value == 0:
                return 0

        return house_parameters
    else:
        return 0

def to_csv (fpath: str):
    print("Началась работа функции [ to_csv ]\n")

    start_time = time.time()
    counter = 1
    houses_urls = get_houses_urls ()
    houses_parameters = []

    for url in houses_urls:
        print(f"Обрабатывается ссылка {url} | {counter}/{len(houses_urls)}", end=" ")
        response = get_house_parameters(url)
        if response != 0:
            houses_parameters.append(response)
            print("| cсылка обработана", end="\n")
        else: print(end="\n")
        counter+=1
    
    print(f"\nКоличество обработанных строк = {len(houses_parameters)}")
    print(f"Ссылок необработано = {len(houses_urls) - len(houses_parameters)}")

    houses_df = pd.DataFrame(data=houses_parameters)
    houses_df.to_csv(fpath)

    end_time = time.time()
    print(f"\nВремя, затраченное на наполнение csv файла = {str(end_time-start_time)[0:4]} сек.")

to_csv ("houses-data.csv")