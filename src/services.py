



def get_sorted_transaction(transactions, user_search):
    """ Функция для поиска транзакций по описанию или категории"""
    filtered_transaction = [transaction for transaction in transactions if user_search.lower() in str(transaction.get("Категория", "")).lower()
                           or user_search.lower() in str(transaction.get("Описание", "")).lower()]
    return filtered_transaction



# if __name__ == "__main__":
    # get_sorted_transaction(transactions_as_list, "фастфуд")
    # print(transactions_as_list)
