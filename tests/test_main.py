from unittest.mock import patch

import json

import pandas as pd

from src.main import get_home_page, get_transactions_by_description, get_filtered_transaction


@patch("src.main.get_stock_prices")
@patch("src.main.get_users_curses")
@patch("src.main.top_transactions_as_period")
@patch("src.main.get_card_spending")
@patch("src.main.greetings")
def test_get_home_page(
    mock_greetings,
    mock_get_card_spending,
    mock_top_transactions_as_period,
    mock_get_users_curses,
    mock_get_stock_prices,
    all_transaction,
):
    """
    Тест успешного выполнения функции.
    """
    mock_greetings.return_value = "Добрый день"
    mock_get_card_spending.return_value = [
        {"cashback": 208, "last_digits": "", "total_spent": 20800.0},
        {"cashback": 5, "last_digits": "*5091", "total_spent": 571.07},
        {"cashback": 4, "last_digits": "*7197", "total_spent": 422.38},
    ]
    mock_top_transactions_as_period.return_value = [
        {"amount": 20000.0, "category": "Переводы", "date": "30.12.2021", "description": "Константин Л."},
        {"amount": 800.0, "category": "Переводы", "date": "31.12.2021", "description": "Константин Л."},
        {"amount": 564.0, "category": "Различные товары", "date": "31.12.2021", "description": "Ozon.ru"},
        {"amount": 160.89, "category": "Супермаркеты", "date": "31.12.2021", "description": "Колхоз"},
        {"amount": 118.12, "category": "Супермаркеты", "date": "31.12.2021", "description": "Магнит"},
    ]
    mock_get_users_curses.return_value = [
        {"currency": "USD", "rate": 88.64},
        {"currency": "EUR", "rate": 92.1},
        {"currency": "RUB", "rate": 1.0},
    ]
    mock_get_stock_prices.return_value = [
        {"price": 236.95, "stock": "AAPL"},
        {"price": 208.65, "stock": "AMZN"},
        {"price": 168.68, "stock": "GOOGL"},
        {"price": 392.655, "stock": "MSFT"},
        {"price": 279.5, "stock": "TSLA"},
    ]
    result = get_home_page(all_transaction, "31.12.2021 23:59:59")
    result_dict = json.loads(result)
    expected_result = {
        "greeting": "Добрый день",
        "cards": [
            {"cashback": 208, "last_digits": "", "total_spent": 20800.0},
            {"cashback": 5, "last_digits": "*5091", "total_spent": 571.07},
            {"cashback": 4, "last_digits": "*7197", "total_spent": 422.38},
        ],
        "top_transactions": [
            {"amount": 20000.0, "category": "Переводы", "date": "30.12.2021", "description": "Константин Л."},
            {"amount": 800.0, "category": "Переводы", "date": "31.12.2021", "description": "Константин Л."},
            {"amount": 564.0, "category": "Различные товары", "date": "31.12.2021", "description": "Ozon.ru"},
            {"amount": 160.89, "category": "Супермаркеты", "date": "31.12.2021", "description": "Колхоз"},
            {"amount": 118.12, "category": "Супермаркеты", "date": "31.12.2021", "description": "Магнит"},
        ],
        "currency_rates": [
            {"currency": "USD", "rate": 88.64},
            {"currency": "EUR", "rate": 92.1},
            {"currency": "RUB", "rate": 1.0},
        ],
        "stock_prices": [
            {"price": 236.95, "stock": "AAPL"},
            {"price": 208.65, "stock": "AMZN"},
            {"price": 168.68, "stock": "GOOGL"},
            {"price": 392.655, "stock": "MSFT"},
            {"price": 279.5, "stock": "TSLA"},
        ],
    }
    assert result_dict == expected_result


@patch("src.main.get_sorted_transaction")
def test_successful_execution(mock_get_sorted_transaction, sample_transactions):
    """Тест успешного выполнения функции."""
    mock_get_sorted_transaction.return_value = [
        {"amount": 100.0, "category": "Супермаркеты", "description": "Покупка в магазине"},
        {"amount": 200.0, "category": "Различные товары", "description": "Покупка на Ozon"},
    ]
    search_str = "Покупка"
    expected_result = [
        {"description": "Покупка в магазине", "category": "Супермаркеты", "amount": 100.0},
        {"description": "Покупка на Ozon", "category": "Различные товары", "amount": 200.0},
    ]
    result = get_transactions_by_description(sample_transactions, search_str)
    result_list = json.loads(result)
    assert result_list == expected_result
    mock_get_sorted_transaction.assert_called_once_with(sample_transactions, search_str)


@patch("src.main.get_sorted_transaction")
def test_exception_successful_execution(mock_get_sorted_transaction, sample_transactions):
    """
    Тест исключения функции.
    """
    mock_get_sorted_transaction.side_effect = ValueError
    search_str = "Покупка"
    expected_result = ""
    result = get_transactions_by_description(sample_transactions, search_str)
    assert result == expected_result
    mock_get_sorted_transaction.assert_called_once_with(sample_transactions, search_str)


@patch("src.main.spending_by_category")
def test_get_filtered_transaction(mock_spending_by_category, all_transaction):
    """Тест успешного выполнения функции."""
    category = "Супермаркеты"
    date = "31.12.2021"
    expected_result = [
        {"Дата операции": "31.12.2021 16:44:00", "Категория": "Супермаркеты", "Сумма операции": -160.89},
        {"Дата операции": "31.12.2021 16:42:04", "Категория": "Супермаркеты", "Сумма операции": -64.00},
        {"Дата операции": "31.12.2021 16:39:04", "Категория": "Супермаркеты", "Сумма операции": -118.12},
        {"Дата операции": "31.12.2021 15:44:39", "Категория": "Супермаркеты", "Сумма операции": -78.05},
    ]
    mock_spending_by_category.return_value = pd.DataFrame(expected_result)
    result = get_filtered_transaction(all_transaction, category, date)
    result_list = json.loads(result)
    assert result_list == expected_result
    mock_spending_by_category.assert_called_once_with(all_transaction, category, date)


@patch("src.main.spending_by_category")
def test_not_category_get_filtered_transaction(mock_spending_by_category, all_transaction):
    """Тест когда нет транзакций по заданной категории."""
    category = "Авиабилеты"
    date = "31.12.2021"
    expected_result = []
    mock_spending_by_category.return_value = pd.DataFrame(expected_result)
    result = get_filtered_transaction(all_transaction, category, date)
    result_list = json.loads(result)
    assert result_list == expected_result
    mock_spending_by_category.assert_called_once_with(all_transaction, category, date)


@patch("src.main.spending_by_category")
def test_exception_get_filtered_transaction(mock_spending_by_category, all_transaction):
    """Тест обработки ошибок в функции."""
    category = "Супермаркеты"
    date = "31.12.2021"
    mock_spending_by_category.side_effect = Exception
    result = get_filtered_transaction(all_transaction, category, date)
    assert result == ""
