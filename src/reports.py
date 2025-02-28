import logging
import os
from datetime import datetime
from typing import Optional

import pandas as pd

from config import LOGS_DIR

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "reports.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Фильтрация транзакций по заданной категории и за период 3 месяца"""
    logger.info("Начало работы")
    try:
        if date is None:
            end_date = datetime.now()  # Если дата не передана, то берется текущая дата
        else:
            end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_date = end_date - pd.DateOffset(months=3)
        logger.info(f"Начальная дата: {start_date}")
        logger.info(f"Конечная дата: {end_date}")
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        transactions.drop(
            transactions[
                ~(
                    (transactions["Категория"].str.lower() == category.lower())
                    & (start_date < transactions["Дата операции"])
                    & (transactions["Дата операции"] <= end_date)
                )
            ].index,
            inplace=True,
        )
        transactions["Дата операции"] = transactions["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")
        logger.info(f"Транзакции отфильтрованы по категории: '{category}'. Найдено транзакций {len(transactions)}")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка в функции spending_by_category: {e}")
        return pd.DataFrame()
