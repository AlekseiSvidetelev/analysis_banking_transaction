import os

import pandas as pd

from config import DATA_DIR

path_file = os.path.join(DATA_DIR, "operations.xlsx")
transactions = pd.read_excel(path_file)
transactions_as_list = transactions.to_dict(orient="records")






if __name__ == "__main__":
    print(transactions)
    print(transactions_as_list)
