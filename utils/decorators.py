import time
from datetime import datetime
from functools import wraps
from zoneinfo import ZoneInfo

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):   
        ist_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%d-%b-%Y %H:%M:%S IST")
        print(f"[LOG] {ist_time} | Action: '{func.__name__}' started")
        start = time.time()

        try:
            result = func(*args, **kwargs)
            end = time.time()
            print(f"[LOG] {ist_time} | Action: '{func.__name__}' completed in {end-start}")
        except Exception as err:
            print(f"[LOG] {ist_time} | Action: '{func.__name__}'" f"raise {type(err).__name__}: {err}")
            raise
        return result
    return wrapper