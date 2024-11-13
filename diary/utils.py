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
    
    changed_year = False

    if direction == "next":
        new_month = month + 1
        if new_month > 12:
            new_month = 1
            changed_year = True
    elif direction == "prev":
        new_month = month - 1
        if new_month < 1:
            new_month = 12
            changed_year = True
    
    return new_month, changed_year

def get_month_first_last_dates(year: int, month: int):
    first_date = datetime(year, month, 1)
    
    last_day = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day)
    
    return first_date, last_date