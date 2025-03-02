import json
import logging
import os
from typing import Any

import pandas as pd

from config import DATA_DIR, LOGS_DIR
from src.decorators import get_record_to_file
from src.reports import spending_by_category
from src.services import get_sorted_transaction
from src.views import get_card_spending, get_stock_prices, get_users_curses, greetings, top_transactions_as_period

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "views.log"), mode="a", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
logger.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


path_file = os.path.join(DATA_DIR, "operations.xlsx")
transactions = pd.read_excel(path_file)
transactions_as_list = transactions.to_dict(orient="records")


def get_home_page(transaction: pd.DataFrame, date: str) -> str:
    """
    Возвращает JSON-ответ с данными пользователя на основе переданного списка транзакций и даты.
        - Приветствие в зависимости от времени суток.
        - По каждой карте:
            - Последние 4 цифры карты.
            - Общая сумма расходов.
            - Кешбэк (1 рубль на каждые 100 рублей).
        - Топ-5 транзакций по сумме платежа.
        - Курс валют.
        - Стоимость акций из S&P500.
    """
    logger.info("Начало работы")
    try:
        main_information = {
            "greeting": greetings(),
            "cards": get_card_spending(transaction, date),
            "top_transactions": top_transactions_as_period(transaction, date),
            "currency_rates": get_users_curses(),
            "stock_prices": get_stock_prices(),
        }
        json_data = json.dumps(main_information, indent=4, ensure_ascii=False)
        logger.info("Функция успешно выполнила обработку.")
        return json_data
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка {Exception}: {e}")
        return ""


def get_transactions_by_description(transactions: list[dict[str, Any]], search_str: str) -> str:
    """Возвращается JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории"""
    logger.info("Начало работы")
    try:
        sorted_transaction = get_sorted_transaction(transactions, search_str)
        logger.info("Функция успешно выполнила обработку.")
        return json.dumps(sorted_transaction, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка {Exception}: {e}")
        return ""


@get_record_to_file("report.txt")
def get_filtered_transaction(transactions: pd.DataFrame, category: str, date: str) -> str:
    """Функция возвращает траты по заданной категории за последние три месяца от заданной даты"""
    logger.info("Начало работы")
    try:
        result = spending_by_category(transactions, category, date)
        result_to_dict = result.to_dict(orient="records")
        logger.info("Функция успешно выполнила обработку.")
        return json.dumps(result_to_dict, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка {Exception}: {e}")
        return ""


# if __name__ == "__main__":
#     print(transactions)
#     print(transactions_as_list)
#     get_home_page(transactions, "31.12.2020 12:00:00")
#     print(get_transactions_by_description(transactions_as_list, "фастфуд"))
#     print(type(get_transactions_by_description(transactions_as_list, "фастфуд")))
#     print(get_filtered_transaction(transactions, "каршеринг", "2021-10-12 00:00:00"))
