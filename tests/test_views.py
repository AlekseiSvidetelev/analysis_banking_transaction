from datetime import datetime
from unittest.mock import patch

import pytest

from src.views import greetings, get_card_spending, top_transactions_as_period, get_users_curses, get_stock_prices


@pytest.mark.parametrize(
    "x, expected",
    [
        (datetime(2025, 2, 28, 10, 0), "Доброе утро"),
        (datetime(2025, 2, 28, 15, 0), "Добрый день"),
        (datetime(2025, 2, 28, 19, 0), "Добрый вечер"),
        (datetime(2025, 2, 28, 2, 0), "Доброй ночи"),
    ],
)
def test_greetings(x, expected):
    """Тест функции приветствия"""
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value = x
        assert greetings() == expected


def test_get_card_spending(test_transactions_list):
    """Тест функции вывода информации по картам"""
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.strptime.return_value = datetime(2025, 2, 28, 23, 59, 59)
        result = get_card_spending(test_transactions_list, "28.02.2025 23:59:59")
        expected_result = [
            {
                "last_digits": "*4556",
                "total_spent": 300,
                "cashback": 3,
            },
            {
                "last_digits": "*5091",
                "total_spent": 200,
                "cashback": 2,
            },
            {
                "last_digits": "*7197",
                "total_spent": 100,
                "cashback": 1,
            },
        ]
        assert result == expected_result


def test_except_get_card_spending(test_transactions_list):
    """Тест обработки исключений данных трат по картам"""
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.strptime.side_effect = ValueError
        result = get_card_spending(test_transactions_list, "except_date")
        assert result == []


def test_top_transactions_as_period(test_transactions_list):
    """Функция для тестирования топ транзакций"""
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.strptime.return_value = datetime(2025, 2, 28, 23, 59, 59)
        result = top_transactions_as_period(test_transactions_list, "28.02.2025 23:59:59")
        expected_result = [
            {"amount": 300, "category": "Транспорт", "date": "20.02.2025", "description": "Bars 2"},
            {
                "amount": 200,
                "category": "Каршеринг",
                "date": "26.02.2025",
                "description": "Ситидрайв",
            },
            {
                "amount": 100,
                "category": "Фастфуд",
                "date": "27.02.2025",
                "description": "Rumyanyj Khleb",
            },
        ]
        assert result == expected_result


def test_except_top_transactions_as_period(test_transactions_list):
    """Функция для тестирования исключений топ транзакций"""
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.strptime.side_effect = ValueError
        result = top_transactions_as_period(test_transactions_list, "except_date")
        assert result == []


@patch("requests.get")
def test_get_users_curses_success(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0, "USD": 1.0, "ALL": 95.293012, "EUR": 0.95}}
    assert get_users_curses() == [
        {"currency": "USD", "rate": 90.0},
        {"currency": "EUR", "rate": 94.74},
        {"currency": "RUB", "rate": 1.0},
    ]


def test_except_get_users_curses_exception():
    with patch("src.views.requests.get") as mock_get:
        mock_get.side_effect = Exception("API error")
        result = get_users_curses()
        assert result == []

@pytest.fixture
def mock_user_settings():
    return {"user_stocks": ["AAPL", "GOOGL"]}

@patch("requests.get")
def test_get_stock_prices(mock_get):
    answer_1.json.return_value = {'adjClose': 237.3, 'adjHigh': 242.46, 'adjLow': 237.06, 'adjOpen': 239.41, 'adjVolume': 41153639, 'close': 237.3, 'date': '2025-02-27T00:00:00+00:00', 'divCash': 0.0, 'high': 242.46, 'low': 237.06, 'open': 239.41, 'splitFactor': 1.0, 'volume': 41153639}
    assert get_stock_prices() == [[]]
"""
[{'adjClose': 237.3, 'adjHigh': 242.46, 'adjLow': 237.06, 'adjOpen': 239.41, 'adjVolume': 41153639, 'close': 237.3, 'date': '2025-02-27T00:00:00+00:00', 'divCash': 0.0, 'high': 242.46, 'low': 237.06, 'open': 239.41, 'splitFactor': 1.0, 'volume': 41153639}]
[{'adjClose': 208.74, 'adjHigh': 219.97, 'adjLow': 208.37, 'adjOpen': 218.35, 'adjVolume': 40548571, 'close': 208.74, 'date': '2025-02-27T00:00:00+00:00', 'divCash': 0.0, 'high': 219.97, 'low': 208.37, 'open': 218.35, 'splitFactor': 1.0, 'volume': 40548571}]
[{'adjClose': 168.5, 'adjHigh': 174.56, 'adjLow': 167.94, 'adjOpen': 173.99, 'adjVolume': 39991015, 'close': 168.5, 'date': '2025-02-27T00:00:00+00:00', 'divCash': 0.0, 'high': 174.56, 'low': 167.94, 'open': 173.99, 'splitFactor': 1.0, 'volume': 39991015}]
[{'adjClose': 392.53, 'adjHigh': 405.74, 'adjLow': 392.17, 'adjOpen': 401.265, 'adjVolume': 21127406, 'close': 392.53, 'date': '2025-02-27T00:00:00+00:00', 'divCash': 0.0, 'high': 405.74, 'low': 392.17, 'open': 401.265, 'splitFactor': 1.0, 'volume': 21127406}]
[{'adjClose': 281.95, 'adjHigh': 297.23, 'adjLow': 280.88, 'adjOpen': 291.16, 'adjVolume': 101748197, 'close': 281.95, 'date': '2025-02-27T00:00:00+00:00', 'divCash': 0.0, 'high': 297.23, 'low': 280.88, 'open': 291.16, 'splitFactor': 1.0, 'volume': 101748197}]
[{'stock': 'AAPL', 'price': 239.41}, {'stock': 'AMZN', 'price': 218.35}, {'stock': 'GOOGL', 'price': 173.99}, {'stock': 'MSFT', 'price': 401.265}, {'stock': 'TSLA', 'price': 291.16}]
"""

def test_except_get_stock_prices():
    with patch("src.views.requests.get") as mock_get:
        mock_get.side_effect = Exception("API error")
        result = get_stock_prices()
        assert result == []

