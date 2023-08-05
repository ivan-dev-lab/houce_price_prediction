import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \brief Стартовый URL-адрес, который ведет на страницу с недвижимостью в Свердловской области
START_URL = "https://dom.mirkvartir.ru/%D0%A1%D0%B2%D0%B5%D1%80%D0%B4%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C/%D0%97%D0%B0%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/"

## \brief Функция парсит все ссылки с недвижимотью со стартового адреса ( START_URL )
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param None
## \details Проверка ссылки, тк не все URL-адреса из START_URL ведут на страницу с описанием недвижимости:
## \code
# urls_ResultSet = soup.find_all("a", {"class": "OffersListItem_offerTitle__3GQ_0"})
# for link in urls_ResultSet:
#     if "Дом" in link.next_element.text:
#         houses_urls.append(link.attrs["href"])
#     else:
#         continue
## \endcode
## \return Список list() с URL-адресами на недвижимость
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

## \brief Функция парсит параметры дома из URL-адреса
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \brief Отдельный парсинг цены на недвижимость
## \param [in] house_url Передается как URL-адрес, ведущий на страницу с продажей недвижимости
## \details Все параметры, кроме цены берутся в цикле, тк блок с ценой находится в другой части
## \code
# house_parameters["price"] = soup.find("div", {"class": "price m-all"}).next_element.text.replace("\u2009", "")
## \endcode
## \brief Перевод данных из ResultSet в list()
## \details Тип данных ResultSet из bs4.BeautifulSoup хранит в себе элементы DOM ( т.е <div class='sc-1u2rf9n'...). Программа получает из div только текст
## \code
# parent_parameter_div_ResultSet = soup.find_all("div", {"class": "sc-1u2rf9n cktnNC"})
# parameters_list = []
# for child in parent_parameter_div_ResultSet:
#     parameters_list.append(child.text)
## \endcode
## \brief Парсинг остальных параметров недвижимости
## \details В первом if программа проверяет, что минимальное количество параметров дома на странице заявлено
## \details В цикле и последующих if программа проверяет, что необходимые параметры присутсвуют на странице
## \code
# if len(parameters_list) >= 4:
#     for parameter in parameters_list:
#         if parameter.find("Площадь") != -1:
#             house_parameters["area_house"] = float(parameter.replace("Площадь", "")[0:3])
#             if parameter.find("участок") != -1:
#                 house_parameters["area_land"] = float(parameter.split("участок ")[1][:-6])
#         elif parameter.find("Тип участка") != -1:
#             house_parameters["type"] = parameter.replace("Тип участка", "")
#         elif parameter.find("Дом") != -1:
#             house_parameters["house_material"] = parameter.replace("Дом", "")
#         elif parameter.find("Этажность") != -1:
#             house_parameters["num_of_floors"] = int(parameter.replace("Этажность", "")[0])
#   ...
# else:
#   return 0
## \endcode
## \brief Проверка полученных данных
## \details В цикле проверяется, что все строковые параметры в house_parameters заполнены, а числовые != 0 | 0.0 ( значение по умолчанию )
## \details Если такие параметры имеются, то программа возврвщает 0, что для функции to_csv - пропуск 
## \code
# for value in house_parameters.values():
#     if value == "" or value == 0.0 or value == 0:
#         return 0
## \endcode
## \return Словарь dict() с параметрами одного дома из URL-адреса

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

## \brief Функция парсит параметры дома из URL-адреса
## \authors ivan-dev-lab
## \version 1.0.0
## \date 05.08.2023
## \param [in] fpath Передается как путь для сохранения необработанного csv файла
## \details В houses_parameters передается dict , содержащий все параметры об одном дома
## \code
# houses_parameters = []
# counter = 1
# for url in houses_urls:
#     print(f"Обрабатывается ссылка {url} | {counter}/{len(houses_urls)}", end=" ")
#     response = get_house_parameters(url)
#     if response != 0:
#         houses_parameters.append(response)
#         print("| cсылка обработана", end="\n")
#     else: print(end="\n")
#     counter+=1
## \endcode
## \return None
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
