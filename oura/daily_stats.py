import json
import pandas as pd

from oura.oura_api import OuraAPI
from models.oura_models import DailyReadiness, DailySleep

DATA_MODELS = dict(
    readiness= DailyReadiness,
    sleep=DailySleep
    )


class DailyData:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date


    def get_combined_daily_data(self):
        readiness_df = self._format_daily_stats('readiness')
        sleep_df = self._format_daily_stats('sleep')
        return readiness_df.set_index('day').join(
            sleep_df.set_index('day'), lsuffix='_readiness', rsuffix='_sleep'
        ).reset_index().sort_values(['day'])


    def retrieve_oura_data(self, endpoint):
        oura_api = OuraAPI()
        return json.loads(oura_api.get_data(endpoint, self.start_date, self.end_date))['data']
        

    def _format_daily_stats(self, data_type):
        raw_data = self.retrieve_oura_data(f'daily_{data_type}')
        daily_stats = [DATA_MODELS[data_type](**s) for s in raw_data]
        daily_stats_df = pd.DataFrame([s.dict() for s in daily_stats])
        return self._flatten_df(daily_stats_df,'contributors')

    
    def _flatten_df(self, df, column_to_flatten):
        flattened_df = pd.DataFrame(df).explode(column_to_flatten).join(
            pd.json_normalize(df[column_to_flatten]))
        del flattened_df[column_to_flatten]
        return flattened_df.drop_duplicates()