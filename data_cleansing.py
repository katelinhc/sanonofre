import pandas as pd
import numpy as np

class DataCleansing():
    def __init__(self, df: pd.DataFrame, data_type: str) -> None:
        self.df_raw = df
        self.data_type = data_type
        self.df = self.df_raw[self.df_raw.data_type == self.data_type][['timestamp','value']]


    def clean_data(self):
        return self._interpolate(self.df)


    def _interpolate(self, df: pd.DataFrame):
        starting_size = len(df)
        nan_vals = df.isna().sum()[0]
        df = self.df.interpolate()
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        print(f'{starting_size - len(df.dropna())} rows dropped, {nan_vals} rows interpolated out of {starting_size} rows')
        return df.dropna().reset_index()
    