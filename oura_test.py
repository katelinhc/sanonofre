# https://cloud.ouraring.com/v2/docs#tag/Daily-Activity-Routes

from dotenv import load_dotenv

from oura.events import EventData
from oura.daily_stats import DailyData
from data_cleansing import DataCleansing 
from data_fitting import DataFitting
from helpers import save_recent_data
from plots import autocorrelation_plt, time_series_plt, fit_sine_plt

START_DATE = '2023-04-12'
END_DATE = '2023-04-30'

def pull_events():
    event_data = EventData(START_DATE, END_DATE)
    return event_data.get_combined_events()

def pull_daily_stats():
    daily_data = DailyData(START_DATE, END_DATE)
    return daily_data.get_combined_daily_data()

def clean_data():
    daily_cleansing=DataCleansing(events, 'heart_rate')
    return daily_cleansing.clean_data()
    
def fit_data(df):
    data_fitter = DataFitting(df, 'heart_rate')
    data_fitter.fit_data()

if __name__ == "__main__":
    load_dotenv()
    events = pull_events()
    # print(events)
    # print(events[events.data_type=='heart_rate'].dropna().rename({'timestamp':'Timestamp'}, axis=1))
    # save_recent_data('events', events, START_DATE)
    # autocorrelation_plt(events, 'heart_rate')
    # fit_sine_plt(events, 'heart_rate')
    # daily_stats = pull_daily_stats()
    # print(daily_stats.iloc[0])
    clean_df = clean_data()
    fit_data(clean_df)
    



