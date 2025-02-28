from unittest.mock import patch

import pandas as pd
from src.reports import spending_by_category
from datetime import datetime



@patch("src.reports.datetime")
def test_spending_by_category(mock_datetime, test_transactions):
    mock_datetime.now.return_value = datetime(2025, 2, 28)
    result = spending_by_category(test_transactions, "Фастфуд")
    expected_result = pd.DataFrame(
        {
        "Дата операции": ["27.02.2025 11:59:39"],
        "Статус": ["OK"],
        "Категория": ["Фастфуд"],
        "Сумма платежа": [-100]
        }
    )
    assert result.equals(expected_result)


@patch("src.reports.datetime")
def test_except_spending_by_category(mock_datetime, test_transactions):
    mock_datetime.now.return_value = datetime(2025, 2, 28)
    result = spending_by_category(test_transactions, [])
    assert result.empty
