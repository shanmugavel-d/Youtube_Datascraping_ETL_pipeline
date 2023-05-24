from datetime import timedelta
from datetime import datetime

def convert_str_to_int(data):
    for key, value in data.items():
        if isinstance(value, str):
            try:
                data[key] = int(value)
            except ValueError:
                pass  # Ignore if the string cannot be converted to an integer
    return data

def convert_duration_to_seconds(duration):
    duration = duration[2:]  # Remove 'PT' from the beginning of the string
    time_delta = timedelta()
    
    if 'H' in duration:
        hours = int(duration.split('H')[0])
        time_delta += timedelta(hours=hours)
        duration = duration.split('H')[1]
    
    if 'M' in duration:
        minutes = int(duration.split('M')[0])
        time_delta += timedelta(minutes=minutes)
        duration = duration.split('M')[1]
    
    if 'S' in duration:
        seconds = int(duration.split('S')[0])
        time_delta += timedelta(seconds=seconds)
    
    total_seconds = time_delta.total_seconds()
    return total_seconds


def convert_to_mysql_datetime(published_at):
    datetime_obj = datetime.fromisoformat(published_at)
    mysql_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_datetime