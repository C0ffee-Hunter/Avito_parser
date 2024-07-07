# Avito_parser

Парсер объявлений Avito

Краткое описание:
Этот проект представляет собой парсер для сбора данных с сайта Avito, созданный в 2021 - 2022 году для изучения библиотек для парсинга данных с сайта. Он извлекает информацию об объявлениях, таких как название товара, ссылка на объявление, цена, дата появления, описание, статус и рейтинг продавца. Данные сохраняются в формате JSON.

Основные функции:
Сбор данных:
- Парсер выполняет HTTP-запрос к странице поиска на Avito с использованием указанного ключевого слова.
- Извлекает HTML-код страницы и сохраняет его локально.
- Анализирует HTML-код с использованием BeautifulSoup для нахождения объявлений.

Извлечение информации:
- Для каждого объявления извлекаются следующие данные:
- Название товара
- Ссылка на объявление
- Цена товара и валюта
- Дата появления товара
- Описание товара
- Статус товара (резервирование)
- Рейтинг продавца
  
Сохранение данных:
- Собранные данные сохраняются в формате JSON.
- Временные HTML-файлы удаляются после обработки для освобождения места.
  
Технологии:
Проект был написан на языке Python. Используемые библиотеки: Requests, BeautifulSoup
  
