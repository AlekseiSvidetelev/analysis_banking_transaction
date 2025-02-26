import os
from cmath import nan
from collections import defaultdict

from dateutil.relativedelta import relativedelta

from config import DATA_DIR
import json
import pandas as pd
from datetime import datetime


def load_user_setting():
    """ Загружает пользовательские настройки из файла data.user_settings.json """
    try:
        with open(os.path.join(DATA_DIR, "user_settings.json"), "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Ошибка {Exception}: {e}")
        return {"user_currencies": [], "user_stocks": []}


def sorted_transactions_as_date(transactions, start_date, end_date):
    """ Функция для фильтрации транзакций за указанный период """
    df = pd.DataFrame(transactions)
    df["Дата операции"] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    filtered_df = df.loc[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
    return filtered_df


# def format_date(date):
#     """ Преобразует значение даты в формат """
#     date_str = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
#     new_format = date_str.strftime("%Y.%m.%d %H:%M:%S")
#     return new_format




# def filtered_curses(curses_dict):
#     """ Функция для фильтрации валюты из пользовательских настроек """
#     try:
#         user_setting = load_user_setting()
#         user_currencies = user_setting.get("user_currencies", [])
#         filtered_rates = {
#             "start_date": curses_dict["start_date"],
#             "end_date": curses_dict["end_date"],
#             "base": curses_dict["base"]
#         }
#         for date, rates in curses_dict["rates"].items():
#             filtered_rates[date] = {currency: rates[currency] for currency in user_currencies if currency in rates}
#         return filtered_rates
#     except Exception as e:
#         print(f"Ошибка {Exception}: {e}")
#
#
# def filtered_stock_prices(prices):
#     """ Функция для фильтрации акций из настроек пользователя """
#     pass
#
#
# def get_transactions_xlsx(path_file):
#     """ Функция для получения данных из файла .xlsx """
#     try:
#         df = pd.read_excel(path_file)
#         list_operations = df.to_dict("records")
#         return list_operations
#     except Exception as e:
#         print(f"Ошибка: {Exception} - {e}")
#
#
# def filtered_operations_by_date(operations_list, date, range_date="M"):
#     """ Функция для фильтрации транзакций за указанный диапазон времени """
#     try:
#         end_date = datetime.strptime(date, "%d.%m.%Y")
#         if range_date == "M":
#             start_date = end_date - relativedelta(months=1)
#         elif range_date == "W":
#             start_date = end_date - relativedelta(weeks=1)
#         elif range_date == "Y":
#             start_date = end_date - relativedelta(years=1)
#         elif range_date == "ALL":
#             start_date = end_date - relativedelta(years=10)
#         filtered_operations = [operation for operation in operations_list if start_date <= (datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")) <= end_date]
#         return filtered_operations
#     except Exception as e:
#         print(f"Ошибка: {Exception} - {e}")
#
#
# def top_category(operations_list):
#     """ Функция 7 основных категорий по тратам """
#     category_list = {}
#     for operation in operations_list:
#         if not pd.isna(operation['MCC']):
#             category = operation["Категория"]
#             amount = abs(operation["Сумма операции"])
#             if category in category_list:
#                 category_list[category] += int(amount)
#             else:
#                 category_list[category] = int(amount)
#     sorted_categories = sorted(category_list.items(), key=lambda x: x[1], reverse=True)
#     top_7_category = sorted_categories[:7]
#     result = dict(top_7_category)
#     new_list = []
#     for key, value in result.items():
#         new_list.append(
#             {"category": key,
#              "amount": value}
#             )
#     return new_list
#
#
# def card_amount_sum(operations_list):
#     """ Функция возвращает траты по картам """
#     card_amount = {}
#     for operation in operations_list:
#         if not pd.isna(operation['Номер карты']):
#             card_number = operation['Номер карты']
#             amount = abs(operation["Сумма платежа"])
#             if card_number in card_amount:
#                 card_amount[card_number] += int(amount)
#             else:
#                 card_amount[card_number] = int(amount)
#
#
#     print(card_amount)





if __name__ == "__main__":
    # print(load_user_setting())
    # print(filtered_curses())
    # path_file_ = os.path.join(DATA_DIR, "operations.xlsx")
    # print(get_transactions_xlsx(path_file_))
    print(format_date("31.12.2021 16:39:04"))

    # filtered_operations_by_date(get_transactions_xlsx(path_file_), "31.12.2021", "M")
    # print(filtered_operations_by_date(get_transactions_xlsx(path_file_), "31.12.2021", "W"))
    # filtered_operations_by_date(get_transactions_xlsx(path_file_), "31.12.2021", "Y")
    # filtered_operations_by_date(get_transactions_xlsx(path_file_), "31.12.2021", "ALL")
    # print(top_category(filtered_operations_by_date(get_transactions_xlsx(path_file_), "31.12.2021", "M")))

    # card_amount_sum(filtered_operations_by_date(get_transactions_xlsx(path_file_), "31.12.2021", "M"))


    otvet = {
        "success": True,
        "timeseries": True,
        "start_date": "2025-02-01",
        "end_date": "2025-02-02",
        "base": "EUR",
        "rates": {
            "2025-02-01": {
                "AED": 3.806062,
                "AFN": 78.367375,
                "ALL": 99.666662,
                "AMD": 414.886103,
                "ANG": 1.869937,
                "AOA": 472.514554,
                "ARS": 1090.727365,
                "AUD": 1.6614,
                "AWG": 1.867778,
                "AZN": 1.76568,
                "BAM": 1.955734,
                "BBD": 2.09493,
                "BDT": 126.525762,
                "BGN": 1.955734,
                "BHD": 0.391187,
                "BIF": 3071.197128,
                "BMD": 1.036215,
                "BND": 1.408053,
                "BOB": 7.16976,
                "BRL": 6.053612,
                "BSD": 1.037565,
                "BTC": 1.018875e-05,
                "BTN": 89.827991,
                "BWP": 14.451516,
                "BYN": 3.395486,
                "BYR": 20309.819708,
                "BZD": 2.08413,
                "CAD": 1.506813,
                "CDF": 2956.322601,
                "CHF": 0.94437,
                "CLF": 0.037078,
                "CLP": 1023.10573,
                "CNY": 7.447076,
                "CNH": 7.585656,
                "COP": 4309.555648,
                "CRC": 523.382469,
                "CUC": 1.036215,
                "CUP": 27.459705,
                "CVE": 110.261307,
                "CZK": 25.201071,
                "DJF": 184.763811,
                "DKK": 7.462864,
                "DOP": 64.097853,
                "DZD": 140.180305,
                "EGP": 52.046257,
                "ERN": 15.543229,
                "ETB": 132.907048,
                "EUR": 1,
                "FJD": 2.407077,
                "FKP": 0.853413,
                "GBP": 0.836177,
                "GEL": 2.96398,
                "GGP": 0.853413,
                "GHS": 15.874468,
                "GIP": 0.853413,
                "GMD": 75.129599,
                "GNF": 8968.699587,
                "GTQ": 8.025731,
                "GYD": 217.072729,
                "HKD": 8.075117,
                "HNL": 26.431115,
                "HRK": 7.6468,
                "HTG": 135.715454,
                "HUF": 407.802929,
                "IDR": 16947.560142,
                "ILS": 3.711614,
                "IMP": 0.853413,
                "INR": 89.696354,
                "IQD": 1359.154474,
                "IRR": 43624.664125,
                "ISK": 146.687036,
                "JEP": 0.853413,
                "JMD": 163.634519,
                "JOD": 0.734888,
                "JPY": 160.828389,
                "KES": 133.845517,
                "KGS": 90.617425,
                "KHR": 4174.86016,
                "KMF": 489.974798,
                "KPW": 932.593877,
                "KRW": 1510.574324,
                "KWD": 0.319652,
                "KYD": 0.864671,
                "KZT": 537.641991,
                "LAK": 22573.243893,
                "LBP": 92912.887816,
                "LKR": 309.199643,
                "LRD": 206.473084,
                "LSL": 19.366651,
                "LTL": 3.059675,
                "LVL": 0.626797,
                "LYD": 5.093829,
                "MAD": 10.414751,
                "MDL": 19.371351,
                "MGA": 4824.838389,
                "MKD": 61.527939,
                "MMK": 2175.678859,
                "MNT": 3521.059671,
                "MOP": 8.328621,
                "MRU": 41.564608,
                "MUR": 48.339835,
                "MVR": 15.96847,
                "MWK": 1799.139737,
                "MXN": 21.427637,
                "MYR": 4.616379,
                "MZN": 66.22491,
                "NAD": 19.366651,
                "NGN": 1557.431939,
                "NIO": 38.178721,
                "NOK": 11.736734,
                "NPR": 143.725186,
                "NZD": 1.838842,
                "OMR": 0.398917,
                "PAB": 1.037565,
                "PEN": 3.859771,
                "PGK": 4.224858,
                "PHP": 60.536773,
                "PKR": 289.399406,
                "PLN": 4.213559,
                "PYG": 8183.72588,
                "QAR": 3.782073,
                "RON": 4.975288,
                "RSD": 117.126077,
                "RUB": 102.196577,
                "RWF": 1472.750669,
                "SAR": 3.886799,
                "SBD": 8.759842,
                "SCR": 14.862476,
                "SDG": 622.765742,
                "SEK": 11.502156,
                "SGD": 1.406355,
                "SHP": 0.853413,
                "SLE": 23.703464,
                "SLL": 21728.916467,
                "SOS": 592.980138,
                "SRD": 36.370643,
                "STD": 21447.564418,
                "SVC": 9.078696,
                "SYP": 13472.718941,
                "SZL": 19.354352,
                "THB": 35.018935,
                "TJS": 11.34562,
                "TMT": 3.637116,
                "TND": 3.313889,
                "TOP": 2.426924,
                "TRY": 37.136661,
                "TTD": 7.037764,
                "TWD": 34.138152,
                "TZS": 2645.71138,
                "UAH": 43.270951,
                "UGX": 3819.872051,
                "USD": 1.036215,
                "UYU": 44.898496,
                "UZS": 13462.549062,
                "VES": 60.484509,
                "VND": 25988.279504,
                "VUV": 123.02156,
                "WST": 2.90226,
                "XAF": 655.935029,
                "XAG": 0.0331,
                "XAU": 0.00037,
                "XCD": 2.800424,
                "XDR": 0.793173,
                "XOF": 655.935029,
                "XPF": 119.331742,
                "YER": 257.888119,
                "ZAR": 19.350081,
                "ZMK": 9327.184796,
                "ZMW": 29.026028,
                "ZWL": 333.660901,
            },
            "2025-02-02": {
                "AED": 3.763725,
                "AFN": 78.615907,
                "ALL": 99.982741,
                "AMD": 416.201859,
                "ANG": 1.875868,
                "AOA": 467.265386,
                "ARS": 1090.859953,
                "AUD": 1.667964,
                "AWG": 1.847031,
                "AZN": 1.741547,
                "BAM": 1.961937,
                "BBD": 2.101574,
                "BDT": 126.927022,
                "BGN": 1.961937,
                "BHD": 0.392427,
                "BIF": 3080.937021,
                "BMD": 1.024705,
                "BND": 1.412518,
                "BOB": 7.192498,
                "BRL": 5.986318,
                "BSD": 1.040856,
                "BTC": 1.02801e-05,
                "BTN": 90.112869,
                "BWP": 14.497347,
                "BYN": 3.406255,
                "BYR": 20084.222469,
                "BZD": 2.09074,
                "CAD": 1.508243,
                "CDF": 2923.483735,
                "CHF": 0.937918,
                "CLF": 0.037196,
                "CLP": 1026.350374,
                "CNY": 7.364348,
                "CNH": 7.537993,
                "COP": 4323.22283,
                "CRC": 525.042307,
                "CUC": 1.024705,
                "CUP": 27.154689,
                "CVE": 110.610986,
                "CZK": 25.19704,
                "DJF": 185.349765,
                "DKK": 7.461663,
                "DOP": 64.301131,
                "DZD": 140.624868,
                "EGP": 52.051567,
                "ERN": 15.370578,
                "ETB": 133.328545,
                "EUR": 1,
                "FJD": 2.380339,
                "FKP": 0.843934,
                "GBP": 0.83369,
                "GEL": 2.931156,
                "GGP": 0.843934,
                "GHS": 15.924812,
                "GIP": 0.843934,
                "GMD": 74.289638,
                "GNF": 8997.142624,
                "GTQ": 8.051184,
                "GYD": 217.761146,
                "HKD": 7.987833,
                "HNL": 26.514937,
                "HRK": 7.561861,
                "HTG": 136.145858,
                "HUF": 408.846911,
                "IDR": 16759.310181,
                "ILS": 3.663311,
                "IMP": 0.843934,
                "INR": 88.700022,
                "IQD": 1363.464852,
                "IRR": 43140.090166,
                "ISK": 145.056867,
                "JEP": 0.843934,
                "JMD": 164.153464,
                "JOD": 0.72672,
                "JPY": 159.213063,
                "KES": 134.26999,
                "KGS": 89.610291,
                "KHR": 4188.100173,
                "KMF": 484.532097,
                "KPW": 922.234819,
                "KRW": 1493.794915,
                "KWD": 0.316101,
                "KYD": 0.867413,
                "KZT": 539.347051,
                "LAK": 22644.831931,
                "LBP": 93207.548672,
                "LKR": 310.180229,
                "LRD": 207.127886,
                "LSL": 19.42807,
                "LTL": 3.025688,
                "LVL": 0.619834,
                "LYD": 5.109984,
                "MAD": 10.44778,
                "MDL": 19.432785,
                "MGA": 4840.139721,
                "MKD": 61.723067,
                "MMK": 2151.387903,
                "MNT": 3481.948475,
                "MOP": 8.355034,
                "MRU": 41.696424,
                "MUR": 47.802769,
                "MVR": 15.790916,
                "MWK": 1804.845469,
                "MXN": 21.700029,
                "MYR": 4.56504,
                "MZN": 65.488755,
                "NAD": 19.42807,
                "NGN": 1540.132054,
                "NIO": 38.2998,
                "NOK": 11.742661,
                "NPR": 144.180991,
                "NZD": 1.840099,
                "OMR": 0.394477,
                "PAB": 1.040856,
                "PEN": 3.872011,
                "PGK": 4.238257,
                "PHP": 59.864293,
                "PKR": 290.317198,
                "PLN": 4.221796,
                "PYG": 8209.679477,
                "QAR": 3.794068,
                "RON": 4.904967,
                "RSD": 117.497527,
                "RUB": 102.195036,
                "RWF": 1477.421302,
                "SAR": 3.843361,
                "SBD": 8.66254,
                "SCR": 14.908633,
                "SDG": 615.84769,
                "SEK": 11.506164,
                "SGD": 1.402145,
                "SHP": 0.843934,
                "SLE": 23.440139,
                "SLL": 21487.556198,
                "SOS": 594.860695,
                "SRD": 35.966642,
                "STD": 21209.329349,
                "SVC": 9.107488,
                "SYP": 13326.222438,
                "SZL": 19.415731,
                "THB": 34.857909,
                "TJS": 11.381601,
                "TMT": 3.596715,
                "TND": 3.324399,
                "TOP": 2.399961,
                "TRY": 36.778546,
                "TTD": 7.060084,
                "TWD": 33.758982,
                "TZS": 2654.101901,
                "UAH": 43.408179,
                "UGX": 3831.986266,
                "USD": 1.024705,
                "UYU": 45.040886,
                "UZS": 13505.243745,
                "VES": 59.81266,
                "VND": 25699.607119,
                "VUV": 121.655062,
                "WST": 2.870022,
                "XAF": 658.01524,
                "XAG": 0.032984,
                "XAU": 0.000367,
                "XCD": 2.769317,
                "XDR": 0.795689,
                "XOF": 658.01524,
                "XPF": 119.331742,
                "YER": 255.023501,
                "ZAR": 19.487327,
                "ZMK": 9223.577315,
                "ZMW": 29.11808,
                "ZWL": 329.954665,
            },
        },
    }
    # print(filtered_curses(otvet))
