import duckdb
import pandas as pd
import os.path
from datetime import date

PATH = os.path.dirname(os.path.realpath(__file__))

def save_recent_data(table_name: str, new_data: pd.DataFrame, start_date: date) -> None:
    if not os.path.exists(f'{PATH}/{table_name}.parquet'):
        new_data.to_parquet(f'{PATH}/{table_name}.parquet')
    else: 
        new_df = new_data
        duckdb.sql(f'''CREATE TABLE {table_name}_old AS SELECT * FROM '{PATH}/{table_name}.parquet';
                   CREATE TABLE {table_name}_new AS SELECT * FROM new_df;
                   DELETE FROM {table_name}_old WHERE timestamp >= '{start_date}';
                   INSERT INTO {table_name}_old SELECT * FROM {table_name}_new;
                   COPY (SELECT * FROM {table_name}_old) TO '{PATH}/{table_name}.parquet';
                   ''')
    return
