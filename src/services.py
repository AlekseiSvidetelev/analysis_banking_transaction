import logging
import os
from typing import Any

from config import LOGS_DIR

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "services.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
logger.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_sorted_transaction(transactions: list[dict[str, Any]], user_search: str) -> list[dict[str, Any]]:
    """Функция для поиска транзакций по описанию или категории"""
    logger.info("Начало работы")
    try:
        filtered_transaction = [
            transaction
            for transaction in transactions
            if user_search.lower() in str(transaction.get("Категория", "")).lower()
            or user_search.lower() in str(transaction.get("Описание", "")).lower()
        ]
        logger.info(f"Функция успешно выполнила поиск. Найдено {len(filtered_transaction)} транзакций")
        return filtered_transaction
    except Exception as e:
        logger.error(f"Ошибка в функции  - {Exception}: {e}.")
        print(f"Ошибка в функции  - {Exception}: {e}.")
        return []
