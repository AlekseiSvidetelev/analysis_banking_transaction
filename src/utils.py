import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
from dotenv import load_dotenv


from config import DATA_DIR

load_dotenv()

API_KEY_stock = os.environ.get("API_KEY_stock")


def load_user_setting() -> Any:
    """Загружает пользовательские настройки из файла data.user_settings.json"""
    try:
        with open(os.path.join(DATA_DIR, "user_settings.json"), "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Ошибка {Exception}: {e}")
        return {"user_currencies": [], "user_stocks": []}


def sorted_transactions_as_date(transactions: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Функция для фильтрации транзакций за указанный период"""
    df = pd.DataFrame(transactions)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered_df = df.loc[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    return filtered_df


if __name__ == "__main__":
    print(load_user_setting())
