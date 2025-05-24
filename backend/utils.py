from models import FrequencyEnum
from datetime import date, timedelta, time

def calculate_dates_to_check(start:date, end:date, frequency: FrequencyEnum):
    if frequency == "daily":
        t = timedelta(days=1)
    else:
        raise Exception("havent coded it")
    
    dates_list:list[date] = []
    
    d = start
    while d < end:
        d += t
        dates_list.append(d)
    return dates_list


if __name__ == '__main__':
    calculate_dates_to_check(date(2025,2,19),date(2025,5,24),FrequencyEnum.DAILY)