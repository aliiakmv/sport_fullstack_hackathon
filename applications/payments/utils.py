import re
import calendar
import datetime

LUHN_ODD_LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)


def luhn(number):
    """Валидитрует средитные карты по Luhn's Algorithm"""
    try:
        evens = sum(int(x) for x in str(number)[-1::-2])
        odds = sum(LUHN_ODD_LOOKUP[int(x)] for x in str(number)[-2::-2])
        return (evens+odds) % 10 == 0
    except ValueError:
        return False

def expire_date(year, month):
    """Возвращает последний день месяца"""
    weekday, day_count = calendar.monthrange(year, month)
    return datetime.date(year, month, day_count)
