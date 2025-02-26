import os
import time
from functools import wraps

from config import DATA_DIR

def get_record_to_file(file_name: str = "report.txt"):
    """ Декоратор, который записывает результаты в файл """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                log_message = f"{func.__name__}: time execution: {end_time - start_time:7f}. Result: {result}"
                with open(os.path.join(DATA_DIR, file_name), "a", encoding="utf-8") as file:
                    file.write(str(log_message) + "\n")
                return result
            except Exception as e:
                log_message = f"{func.__name__}: error - {str(e)}. Input: {args}, {kwargs}"
                with open(os.path.join(DATA_DIR, file_name), "a", encoding="utf-8") as file:
                    file.write(str(log_message) + "\n")
        return wrapper
    return decorator
