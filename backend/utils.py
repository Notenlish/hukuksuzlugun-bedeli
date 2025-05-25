from datetime import date, timedelta

from models import FrequencyEnum


def calculate_dates_to_check(start: date, end: date, frequency: FrequencyEnum):
    if frequency == "daily":
        t = timedelta(days=1)
    else:
        raise Exception("havent coded it")

    dates_list: list[date] = []

    d = start
    while d < end:
        d += t
        dates_list.append(d)
    return dates_list


def first_day_of_current_month(date_obj: date):
    first_day_of_month = date_obj.replace(day=1)
    return first_day_of_month


def first_day_of_the_next_month(date_obj: date):
    same_time_next_month = date_obj + timedelta(days=date_obj.day)
    first_day_of_next_month = same_time_next_month - timedelta(
        days=same_time_next_month.day - 1
    )
    return first_day_of_next_month


# TODO: I *think* this is how it is supposed to work?
def first_day_of_the_previous_month(date_obj: date):
    first_day_of_month = date_obj.replace(day=1)
    last_day_of_prev_month = first_day_of_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_prev_month.replace(day=1)
    return first_day_of_previous_month

def first_friday_on_or_after(d: date) -> date:
    """Return the first Friday on or after the given date."""
    days_until_friday = (4 - d.weekday()) % 7  # 4 = Friday
    return d + timedelta(days=days_until_friday)

def last_friday_on_or_before(d: date) -> date:
    """Return the last Friday on or before the given date."""
    days_since_friday = (d.weekday() - 4) % 7  # 4 = Friday
    return d - timedelta(days=days_since_friday)


if __name__ == "__main__":
    # calculate_dates_to_check(date(2025, 3, 19),date(2025, 5, 24), FrequencyEnum.DAILY)
    print(first_day_of_the_next_month(date(2025, 3, 19)))
