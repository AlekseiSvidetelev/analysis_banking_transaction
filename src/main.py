import os

import pandas as pd
import json

from config import DATA_DIR
from src.decorators import get_record_to_file

from src.views import greetings
from src.views import get_card_spending
from src.views import top_transactions_as_period
from src.views import get_users_curses
from src.views import get_stock_prices
from src.services import get_sorted_transaction
from src.reports import spending_by_category

path_file = os.path.join(DATA_DIR, "operations.xlsx")
transactions = pd.read_excel(path_file)
transactions_as_list = transactions.to_dict(orient="records")


def get_home_page(transaction, date):
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
    try:
        main_information = {
            "greeting": greetings(),
            "cards": get_card_spending(transaction, date),
            "top_transactions": top_transactions_as_period(transaction, date),
            "currency_rates": get_users_curses(),
            "stock_prices": get_stock_prices(),
        }
        json_data = json.dumps(main_information, indent=4, ensure_ascii=False)
        return json_data
    except Exception as e:
        print(f"Ошибка {Exception}: {e}")


def get_transactions_by_description(transactions, search_str):
    sorted_transaction = get_sorted_transaction(transactions, search_str)
    return json.dumps(sorted_transaction, indent=4, ensure_ascii=False)


@get_record_to_file("report.txt")
def get_filtered_transaction(transactions, category, date):
    result = spending_by_category(transactions, category, date)
    result_to_dict = result.to_dict(orient="records")
    return json.dumps(result_to_dict, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # print(transactions)
    # print(transactions_as_list)
    # get_home_page(transactions, "31.12.2020 12:00:00")
    # print(get_transactions_by_description(transactions_as_list, "фастфуд"))
    # print(type(get_transactions_by_description(transactions_as_list, "фастфуд")))
    print(get_filtered_transaction(transactions, "каршеринг", "2021-10-12 00:00:00"))
