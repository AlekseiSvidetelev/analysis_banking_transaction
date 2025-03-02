from typing import List, Dict, Any

from src.services import get_sorted_transaction


def test_get_sorted_transaction(test_transactions_list: List[Dict[str, Any]]) -> None:
    """Тест работы функции"""
    result = get_sorted_transaction(test_transactions_list, "ситидрайв")
    assert result == [
        {
            "Номер карты": "*5091",
            "Дата операции": "26.02.2025 11:59:39",
            "Описание": "Ситидрайв",
            "Кэшбэк": "sum",
            "Категория": "Каршеринг",
            "Сумма платежа": -200,
        }
    ]


def test_exception_get_sorted_transaction(test_transactions_list: List[Dict[str, Any]]) -> None:
    """Тест обработки исключения"""
    result = get_sorted_transaction(test_transactions_list, {})
    assert result == []
