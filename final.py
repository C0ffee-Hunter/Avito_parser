import io
import json
import os
import time
import requests
from bs4 import BeautifulSoup


def get_data(url, sentence):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"
    }

    # Создание директории data, если она не существует
    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        req = requests.get(url, headers=headers)
        req.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return

    print('здесь')
    with io.open(f"{sentence}.html", "w", encoding="utf-8") as file:
        file.write(req.text)

    data_dict = []
    try:
        with io.open(f"{sentence}.html", encoding="utf-8") as file:
            scr = file.read()

        soup = BeautifulSoup(scr, "lxml")
        articles = soup.find_all("div",
                                 class_="iva-item-content-rejJg")

        for count, article in enumerate(articles):
            interest = int((count / 50) * 100)
            print(f"Progress: {interest}%")
            ad_name = article.find("div", class_="iva-item-title-py3i_").find("a").get("title")
            ad_url = "https://www.avito.ru/" + article.find("div", class_="iva-item-title-py3i_").find("a").get(
                "href")

            try:
                ad_req = requests.get(ad_url, headers=headers)
                ad_req.raise_for_status()
            except requests.RequestException as e:
                print(f"Ошибка при выполнении запроса к {ad_url}: {e}")
                continue

            with io.open(f"data/{count}.html", "w", encoding="utf-8") as file:
                file.write(ad_req.text)

            with io.open(f"data/{count}.html", encoding="utf-8") as file:
                scr1 = file.read()

            ad_soup = BeautifulSoup(scr1, "lxml")
            ad_description_head = ad_soup.find("div", itemprop="description").find("p").text \
                if ad_soup.find("div",itemprop="description") \
                else "Описание отсутствует"

            ad_reservation = ad_soup.find("span", class_="css-79nocf").get_text() if ad_soup.find("span",
                                                                                                  class_="css-79nocf") else "Написать продавцу"
            ad_user_score = ad_soup.find("span", class_="styles-module-size_m-n6S6Y").text.replace('\n', '').replace(' ',
                                                                                                                   '') if ad_soup.find(
                "span", class_="styles-module-size_m-n6S6Y") else "Нет оценки пользователя"
            ad_cost = article.find("meta", itemprop="price").get("content") if article.find("meta",
                                                                                            itemprop="price") else "Цена не указана"
            ad_currency = article.find("meta", itemprop="priceCurrency").get("content") if article.find("meta",
                                                                                                        itemprop="priceCurrency") else ""
            ad_cost1 = ad_cost + " " + ad_currency
            ad_date = article.find("div",
                                   class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI").get_text() if article.find(
                "div",
                class_="date-text-2jSvU text-text-1PdBw text-size-s-1PUdo text-color-noaccent-bzEdI") else "Дата не указана"

            data = {
                "Название товара": ad_name,
                "Ссылка на объявление": ad_url,
                "Цена товара": ad_cost1,
                "Дата появления товара": ad_date,
                "Описание товара": ad_description_head,
                "Статус товара": ad_reservation,
                "Рейтинг продавца": ad_user_score
            }

            data_dict.append(data)
            with open('end_data.json', "w", encoding='utf8') as json_file:
                json.dump(data_dict, json_file, indent=4, ensure_ascii=False)

            os.remove(f"data/{count}.html")

            time.sleep(5)

    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")

    finally:
        os.remove(f"{sentence}.html")


if __name__ == "__main__":
    print("Введите товар, который вы ищите:")
    sentence = str(input()).strip().replace(' ', '+')

    url = f"https://www.avito.ru/rossiya?q={sentence}"

    get_data(url, sentence)