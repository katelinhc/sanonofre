# https://cloud.ouraring.com/v2/docs#tag/Daily-Activity-Routes

from dotenv import load_dotenv

from oura.events import EventData
from oura.daily_stats import DailyData
from helpers import save_recent_data

START_DATE = '2023-04-09'
END_DATE = '2023-04-12'

def pull_events():
    event_data = EventData(START_DATE, END_DATE)
    return event_data.get_combined_events()

def pull_daily_stats():
    daily_data = DailyData(START_DATE, END_DATE)
    return daily_data.get_combined_daily_data()

if __name__ == "__main__":
    load_dotenv()
    events = pull_events()
    print(events)
    save_recent_data('events', events, START_DATE)
    # daily_stats = pull_daily_stats()
    # print(daily_stats.iloc[0])



