import logging
import math
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

from config import LOGS_DIR
from src.utils import load_user_setting, sorted_transactions_as_date

load_dotenv()
API_KEY_currencies = os.environ.get("API_KEY_currencies")
API_KEY_STOCKS = os.environ.get("API_KEY_STOCKS")
API_KEY_curs = os.environ.get("API_KEY_curs")
API_KEY_stock = os.environ.get("API_KEY_stock")


logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "views.log"), mode="a", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
logger.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def greetings() -> str:
    """Функция для приветствия в зависимости от времени запроса"""
    logger.info("Начало работы")
    try:
        hour_now = datetime.now()
        logger.info(f"Время запроса {hour_now}")
        hour = hour_now.hour
        if 4 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 17:
            greeting = "Добрый день"
        elif 17 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"
        logger.info(f"Функция вернула '{greeting}'")
        return greeting
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка в функции - {Exception}: {e}.")
        return ""


def get_card_spending(transactions: DataFrame, date_str: str) -> list[dict[str, Any]]:
    """Получение информации трат по картам"""
    logger.info("Начало работы")
    try:
        end_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0)
        logger.info(f"Диапазон времени для обработки: {start_date} - {end_date}")
        df = pd.DataFrame(transactions)
        sort_transactions = sorted_transactions_as_date(df, start_date, end_date)
        filtered_df = sort_transactions[~(sort_transactions["Сумма платежа"] >= 0)]
        grop_by_card = filtered_df.groupby("Номер карты")
        agg_info = grop_by_card.agg({"Сумма платежа": "sum", "Кэшбэк": "sum"})
        result = agg_info.reset_index()
        to_new_dict = result.to_dict(orient="records")
        result_list = []
        for i in to_new_dict:
            result_list.append(
                {
                    "last_digits": i["Номер карты"],
                    "total_spent": round(abs(i["Сумма платежа"]), 2),
                    "cashback": math.floor(abs(i["Сумма платежа"]) / 100),
                }
            )
        logger.info("Функция успешно выполнила обработку.")
        return result_list
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка в функции - {Exception}: {e}.")
        return []


def top_transactions_as_period(transactions: DataFrame, date_str: str) -> List[Dict[str, Any]]:
    """Функция возвращает топ 5 транзакций по сумме платежа"""
    logger.info("Начало работы")
    try:
        end_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0)
        df = pd.DataFrame(transactions)
        sort_transactions = sorted_transactions_as_date(df, start_date, end_date)
        sorted_df = sort_transactions.sort_values(by="Сумма платежа", ascending=True)
        df_five_transactions = sorted_df.iloc[:5]
        to_new_dict = df_five_transactions.to_dict(orient="records")
        result_list = []
        for category in to_new_dict:
            result_list.append(
                {
                    "date": category["Дата операции"].strftime("%d.%m.%Y"),
                    "amount": round(abs(category["Сумма платежа"]), 2),
                    "category": category["Категория"],
                    "description": category["Описание"],
                }
            )
        logger.info("Функция успешно выполнила обработку.")
        return result_list
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка в функции - {Exception}: {e}.")
        return []


def get_users_curses() -> List[Dict[str, Any]]:
    """Функция возвращает JSON ответ с данными о валютах и акциях за указанный период"""
    logger.info(f"Начало работы - {datetime.now()}")
    try:
        date = datetime.now()
        app_id = API_KEY_curs
        date_for_get = date.strftime("%Y-%m-%d")
        url = f"https://openexchangerates.org/api/historical/{date_for_get}.json?app_id={app_id}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        logger.info(f"Код ответа: {response}")

        data_json = response.json()
        user_setting = load_user_setting()
        user_stocks = user_setting.get("user_currencies", [])
        rub_curs = data_json["rates"]["RUB"]
        filtered_list = []
        for stocks in user_stocks:
            currency = data_json["rates"][stocks]
            currency_in_rubles = 1 / currency * rub_curs
            filtered_list.append(
                {
                    "currency": stocks,
                    "rate": round(currency_in_rubles, 2),
                }
            )
        logger.info("Функция успешно выполнила обработку.")
        return filtered_list
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка в функции - {Exception}: {e}.")
        return []


def get_stock_prices() -> List[Dict[str, Any]]:
    """
    Возвращает цены на акции за указанный период.
    """
    logger.info("Начало работы")
    try:
        user_setting = load_user_setting()
        user_stocks = user_setting.get("user_stocks", [])
        stock_list = []
        for stock in user_stocks:
            ticker = stock
            headers = {"Content-Type": "application/json", "Authorization": f"Token {API_KEY_stock}"}
            requestResponse = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices", headers=headers)
            logger.info(f"Код ответа: {requestResponse}")
            stock_list.append(
                {stock: {k: v for k, v in item.items() if k == "open"} for item in requestResponse.json()}
            )
        result = []
        for stock in stock_list:
            for key, value in stock.items():
                result.append({"stock": key, "price": value["open"]})
        logger.info("Функция успешно выполнила обработку.")
        return result
    except Exception as e:
        logger.error(f"Ошибка в функции - {Exception}: {e}.")
        print(f"Ошибка в функции - {Exception}: {e}.")
        return []


if __name__ == "__main__":
    # print(load_user_setting())
    # print(get_users_curses())
    print(get_stock_prices())
    # print(greetings())
    # get_card_spending(transactions, "31.12.2021 16:44:00")
    # top_transactions_as_period(transactions,"31.12.2021 16:44:00")
