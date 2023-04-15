import requests
import os

class OuraAPI:
    def __init__(self) -> None:
        self.base_url = 'https://api.ouraring.com/v2/usercollection/'
        self.token = os.getenv('TOKEN')

    def get_data(self, endpoint, start_date, end_date) -> str:
        url = f'{self.base_url}{endpoint}'
        params={ 
            'start_date': start_date, 
            'end_date': end_date
        }
        headers = { 
            'Authorization': f'Bearer {self.token}' 
        }
        response = requests.request('GET', url, headers=headers, params=params)
        response.raise_for_status()
        return response.text
            