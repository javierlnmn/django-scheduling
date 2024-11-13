import calendar
from datetime import datetime

def get_next_prev_month(month: int, direction: str) -> tuple:

    if month == 0:
        month = 1

    if month < 0:
        month *= -1

    if month > 12:
        month = month % 12
    
    if direction not in ["next", "prev"]:
        raise ValueError("Direction must be either 'next' or 'prev'")
    
    if direction == "next":
        new_month = month + 1
        if new_month > 12:
            new_month = 1
    elif direction == "prev":
        new_month = month - 1
        if new_month < 1:
            new_month = 12
    
    return new_month

def get_month_first_last_dates(year: int, month: int):
    first_date = datetime(year, month, 1)
    
    last_day = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day)
    
    return first_date, last_date