from datetime import datetime, date, timedelta

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

def serialize_date(d:date):
    return d.strftime("%Y-%m-%d")

def get_dates_between_dates_with_step(start:date, end:date, wanted_point_count:int):
    total_distance = (end - start).total_seconds()
    
    # account for the start and end points.
    step_size = total_distance / (wanted_point_count - 2)
    
    start_of_between_points = datetime.timestamp(datetime(start.year, start.month, start.day)) + (step_size / 2)
    end_of_between_points = datetime.timestamp(datetime(end.year, end.month, end.day)) - (step_size / 2)
    
    # no need to worry about me making it int since these are in seconds
    timepoints = [i for i in range(int(start_of_between_points), int(end_of_between_points), int(step_size))]
    dates = [date.fromtimestamp(i) for i in timepoints]
    return dates

if __name__ == "__main__":
    # calculate_dates_to_check(date(2025, 3, 19),date(2025, 5, 24), FrequencyEnum.DAILY)
    print(first_day_of_the_next_month(date(2025, 3, 19)))
