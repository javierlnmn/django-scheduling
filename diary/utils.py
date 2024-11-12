import calendar
from datetime import datetime

def get_next_month(month: int, direction: str) -> tuple:

    if month == 0:
        month = 1

    if month < 0:
        month *= -1

    if month > 12:
        month = month % 12
    
    if direction not in ["left", "right"]:
        raise ValueError("Direction must be either 'left' or 'right'")
    
    changed_year = False

    if direction == "right":
        next_month = month + 1
        if next_month > 12:
            next_month = 1
            changed_year = True
    elif direction == "left":
        next_month = month - 1
        if next_month < 1:
            next_month = 12
            changed_year = True
    
    return next_month, changed_year

def get_month_first_last_dates(year: int, month: int):
    # Get the first date of the month
    first_date = datetime(year, month, 1)
    
    # Get the last day of the month using calendar.monthrange
    last_day = calendar.monthrange(year, month)[1]
    last_date = datetime(year, month, last_day)
    
    return first_date, last_date