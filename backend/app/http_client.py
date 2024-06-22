import random
import requests
import json
import brotli

from dataclasses import dataclass

@dataclass
class HTTPClient:
    HEADERS = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"',
        "sec-ch-ua-mobile": '?1',
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.64 Mobile Safari/537.36",
        "sec-ch-ua-platform": '"Android"',
        "Accept": "*/*",
        'Accept-Encoding':'gzip, deflate, br, zstd',
        "Origin": "https://hamsterkombat.io",
        "Host": "api.hamsterkombat.io",
        "X-Requested-With": "org.telegram.messenger",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://hamsterkombat.io/",
        'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    def post(self, **kwargs):
        headers = self.HEADERS.copy()
        data = kwargs
        json = None
        token = data['token'] 
        headers['Authorization'] = f'Bearer {token}'
        
        if 'data' in data:
            json = data['data']
        
        try:
            if json:   
                response = requests.post(data['endpoint'], proxies=data['proxy'], json=json, headers=headers)
            else:
                response = requests.post(data['endpoint'], proxies=data['proxy'], headers=headers)
                self.write_file(response, token)
            response.raise_for_status()
            return response.status_code
        except requests.RequestException as e:
            raise Exception(f'BAD REQUEST - {e}')

    def post_get_card(self, **kwargs):
        headers = self.HEADERS.copy()
        data = kwargs
        token = data['token'] 
        headers['Authorization'] = f'Bearer {token}'
        
        try:
            response = requests.post(data['endpoint'], proxies=data['proxy'], headers=headers)
            response.raise_for_status()
            self.write_file_user_card(response, token)
            return response.status_code
        except requests.RequestException as e:
            raise Exception(f'BAD REQUEST - {e}')
        
    def write_file_user_card(
        self, 
        response: requests.Response, 
        token: str
        ):

        with open(f'card_{token}.json', 'wb') as file:
            for chunk in response.iter_content():
                if chunk:
                    file.write(chunk,)

        with open(f'card_{token}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        with open(f'card_{token}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def write_file(
        self, 
        response: requests.Response, 
        token: str
        ):

        with open(f'{token}.json', 'wb') as file:
            for chunk in response.iter_content():
                if chunk:
                    file.write(chunk,)

        with open(f'{token}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        with open(f'{token}.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)