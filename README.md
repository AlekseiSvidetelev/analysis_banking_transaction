# Analysis Banking Transaction
Проект для анализа банковских транзакций, загруженных из Excel-файла. Приложение предоставляет JSON-данные для 
веб-страниц.

# Установка и запуск
Клонируйте репозиторий:
https://github.com/AlekseiSvidetelev/analysis_banking_transaction

Для установки зависимостей и настройки проекта выполните следующие действия:

`-poetry install`

Запустите приложение:

`python src/main.py`

Для запуска тестов:

`pytest tests/`


## Основные функции
Генерация JSON-ответов
JSON-ответы формируются на основе данных из Excel-файла (operations.xls) и пользовательских настроек (user_settings.json).
Данные анализируются с начала месяца, на который выпадает входящая дата, до указанной даты.

Пример JSON-ответа:`{
  "greeting": "Добрый день",
  "cards": [
    {
      "last_digits": "5814",
      "total_spent": 1262.00,
      "cashback": 12.62
    },
    {
      "last_digits": "7512",
      "total_spent": 7.94,
      "cashback": 0.08
    }
  ],
  "top_transactions": [
    {
      "date": "21.12.2021",
      "amount": 1198.23,
      "category": "Переводы",
      "description": "Перевод Кредитная карта. ТП 10.2 RUR"
    },
    {
      "date": "20.12.2021",
      "amount": 829.00,
      "category": "Супермаркеты",
      "description": "Лента"
    },
    {
      "date": "20.12.2021",
      "amount": 421.00,
      "category": "Различные товары",
      "description": "Ozon.ru"
    },
    {
      "date": "16.12.2021",
      "amount": -14216.42,
      "category": "ЖКХ",
      "description": "ЖКУ Квартира"
    },
    {
      "date": "16.12.2021",
      "amount": 453.00,
      "category": "Бонусы",
      "description": "Кешбэк за обычные покупки"
    }
  ],
  "currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },
    {
      "currency": "EUR",
      "rate": 87.08
    }
  ],
  "stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },
    {
      "stock": "AMZN",
      "price": 3173.18
    },
    {
      "stock": "GOOGL",
      "price": 2742.39
    },
    {
      "stock": "MSFT",
      "price": 296.71
    },
    {
      "stock": "TSLA",
      "price": 1007.08
    }
  ]
}`

## Простой поиск

Пользователь может передать строку для поиска, и приложение вернет JSON-ответ со всеми 
транзакциями, содержащими 
запрос в описании или категории.

## Отчеты

Отчеты формируются в отдельном модуле reports.py. Для функций-отчетов реализован декоратор, 
который записывает 
результат в файл:
Декоратор с параметром — принимает имя файла в качестве параметра.

## Траты по категории

Функция принимает:
Название категории.
Опциональную дату (если дата не передана, используется текущая дата).
Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).

## Пример использования

### Генерация JSON-ответа

`from src.main import get_home_page
from datetime import datetime
date = "20.05.2020"
json_response = get_home_page(date)
print(json_response)`

### Поиск транзакций

`from src.main import get_transactions_by_description
search_str = "Перевод"
json_response = get_transactions_by_description(search_str)
print(json_response)`

### Формирование отчета

`from src.reports import spending_by_category
from src.decorators import get_record_to_file
@get_record_to_file("report.txt")
def generate_report():
    transactions = pd.read_excel("data/operations.xls")
    category = "Супермаркеты"
    result = spending_by_category(transactions, category)
    return result
generate_report()  # Отчет будет сохранен в файл report.txt`

### Траты по категории

`from src.reports import spending_by_category
import pandas as pd
transactions = pd.read_excel("data/operations.xls")
category = "Супермаркеты"
spending = spending_by_category(transactions, category)
print(spending)`