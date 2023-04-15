import unittest
import pandas as pd
import pendulum

from mockito import when

from oura.oura_api import OuraAPI
from oura.daily_stats import DailyData


class TestDaiilyStats(unittest.TestCase):
    def test_collect_data(self):
        start_date = '2023-04-11'
        end_date = '2023-04-16'
        when(OuraAPI).get_data('daily_sleep', start_date, end_date).thenReturn(self.mock_daily_sleep())
        when(OuraAPI).get_data('daily_readiness', start_date, end_date).thenReturn(self.mock_daily_readiness())
        
        daily_data = DailyData(start_date, end_date)
        self.assertIsInstance(daily_data.retrieve_oura_data('daily_sleep'), list)
        self.assertIsInstance(daily_data.retrieve_oura_data('daily_readiness'), list)
        
    def test_get_combined_daily_data(self):
        start_date = '2023-04-11'
        end_date = '2023-04-16'
        when(OuraAPI).get_data('daily_sleep', start_date, end_date).thenReturn(self.mock_daily_sleep())
        when(OuraAPI).get_data('daily_readiness', start_date, end_date).thenReturn(self.mock_daily_readiness())
        
        daily_data = DailyData(start_date, end_date)
        combined_daily_data = daily_data.get_combined_daily_data()
        self.assertIsInstance(combined_daily_data, pd.DataFrame)
        self.assertTrue(sorted(list(combined_daily_data['day'])), list(combined_daily_data['day']))
        self.assertTrue(min(combined_daily_data['day'])>=pendulum.parse(start_date).date())
        self.assertTrue(max(combined_daily_data['day'])<pendulum.parse(end_date).date())
        
    def mock_daily_readiness(self):
        return '''{"data":[{"id":"1e8fc04d-bca5-45b2-b5ed-cf90bae60719","contributors":{"activity_balance":null,"body_temperature":85,"hrv_balance":null,"previous_day_activity":null,"previous_night":93,"recovery_index":100,"resting_heart_rate":100,"sleep_balance":null},"day":"2023-04-12","score":97,"temperature_deviation":0.2,"temperature_trend_deviation":null,"timestamp":"2023-04-12T00:00:00+00:00"},
                        {"id":"f48412f7-ec4d-4a60-86cb-3a80eb91d1db","contributors":{"activity_balance":null,"body_temperature":96,"hrv_balance":null,"previous_day_activity":36,"previous_night":74,"recovery_index":80,"resting_heart_rate":100,"sleep_balance":null},"day":"2023-04-13","score":75,"temperature_deviation":0.09,"temperature_trend_deviation":0.0,"timestamp":"2023-04-13T00:00:00+00:00"},
                        {"id":"6c974668-a5f6-4c62-9cc7-09abc636d7e0","contributors":{"activity_balance":85,"body_temperature":88,"hrv_balance":null,"previous_day_activity":100,"previous_night":80,"recovery_index":59,"resting_heart_rate":71,"sleep_balance":82},"day":"2023-04-14","score":79,"temperature_deviation":0.14,"temperature_trend_deviation":0.07,"timestamp":"2023-04-14T00:00:00+00:00"},
                        {"id":"a7088a11-331a-484d-8607-4eec07df0a61","contributors":{"activity_balance":83,"body_temperature":91,"hrv_balance":null,"previous_day_activity":77,"previous_night":77,"recovery_index":74,"resting_heart_rate":100,"sleep_balance":92},"day":"2023-04-15","score":85,"temperature_deviation":0.19,"temperature_trend_deviation":0.24,"timestamp":"2023-04-15T00:00:00+00:00"}],
                        "next_token":null}'''
        
    def mock_daily_sleep(self):
        return '''{"data":[{"id":"751cce67-01d3-40a1-afbc-3ac6dc5a903b","contributors":{"deep_sleep":100,"efficiency":97,"latency":94,"rem_sleep":88,"restfulness":89,"timing":100,"total_sleep":98},"day":"2023-04-12","score":96,"timestamp":"2023-04-12T00:00:00+00:00"},
                    {"id":"523c50cc-cb09-4136-9cb3-0d1c9157ad85","contributors":{"deep_sleep":96,"efficiency":93,"latency":72,"rem_sleep":57,"restfulness":64,"timing":100,"total_sleep":97},"day":"2023-04-13","score":85,"timestamp":"2023-04-13T00:00:00+00:00"},
                    {"id":"8696847f-425f-441f-960b-021e916df3b5","contributors":{"deep_sleep":97,"efficiency":99,"latency":72,"rem_sleep":82,"restfulness":87,"timing":95,"total_sleep":80},"day":"2023-04-14","score":86,"timestamp":"2023-04-14T00:00:00+00:00"},
                    {"id":"43c6d512-fc80-4f01-b92d-e955e1e9139e","contributors":{"deep_sleep":100,"efficiency":76,"latency":75,"rem_sleep":52,"restfulness":74,"timing":100,"total_sleep":91},"day":"2023-04-15","score":83,"timestamp":"2023-04-15T00:00:00+00:00"}],
                    "next_token":null}'''

        
if __name__ == '__main__':
    unittest.main()