import json
import pandas as pd
from datetime import timedelta
from typing import List, Union

from oura.oura_api import OuraAPI
from models.oura_models import Heartrate, Sleep, Tag

DATA_MODELS = dict(heartrate=Heartrate, tag=Tag, sleep=Sleep)
EVENT_TYPES = ['heart_rate', 'hrv']

class EventData: 
    def __init__(self, start_date, end_date): 
        self.start_date = start_date 
        self.end_date = end_date

    def get_combined_events(self) -> pd.DataFrame: 
        hr_events = pd.DataFrame(self._collect_heartrate_events())
        sleep_events = pd.DataFrame(self._collect_sleep_events()) 
        tag_events = pd.DataFrame(self._collect_tag_events()) 
        return pd.concat([hr_events, sleep_events, tag_events]).sort_values(['timestamp'])
    
    def retrieve_oura_data(self, endpoint) -> list: 
        oura_api = OuraAPI() 
        return json.loads(oura_api.get_data(endpoint, self.start_date, self.end_date))['data']
    
    def _collect_sleep_events(self) -> List[dict]: 
        sleep_data = self._format_events_data('sleep')
        sleep_events = []
        for s in sleep_data:
            start_time = s.dict()['bedtime_start']
            for event_type in EVENT_TYPES: 
                interval = s.dict()[event_type]['interval']
                interval_data = s.dict()[event_type]['items']
                sleep_events.extend(
                    dict(
                        timestamp=start_time + timedelta(seconds=i * interval),
                        data_type=event_type,
                        value=interval_data[i],
                    )
                    for i in range(len(interval_data))
                )
        return sleep_events

    def _collect_heartrate_events(self) -> List[dict]: 
        raw_data = self._format_events_data('heartrate')
        return [
            dict(
                timestamp=event.dict()['timestamp'],
                data_type='heart_rate',
                value=event.dict()['bpm'],
            )
            for event in raw_data
        ]

    def _collect_tag_events(self) -> List[dict]: 
        raw_data = self._format_events_data('tag')
        return [
            dict(
                timestamp=event.dict()['timestamp'],
                data_type='tag',
                value=event.dict()['tags'],
            )
            for event in raw_data
        ]

    def _format_events_data(self, data_type) -> List[Union[Heartrate, Tag, Sleep]]: 
        raw_data = self.retrieve_oura_data(data_type)
        return [DATA_MODELS[data_type](**s) for s in raw_data]

    def _flatten_df(self, df, column_to_flatten) -> pd.DataFrame: 
        flattened_df = pd.DataFrame(df).explode(column_to_flatten).join( pd.json_normalize(df[column_to_flatten])) 
        del flattened_df[column_to_flatten] 
        return flattened_df.drop_duplicates()
