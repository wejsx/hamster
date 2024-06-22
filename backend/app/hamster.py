from dataclasses import dataclass
import json

import time
from typing import Optional, Dict, List


from storage_model import Storage
from user_model import UserModel

from http_client import HTTPClient
from log import logger
from schemas import MorseHamsterSchema, CardSchema

from const import (
    URL_INFO_SYNC, 
    URL_TAP, 
    URL_MORSE, 
    URL_GET_MY_CARD, 
    CARDS_UPDATE,
    URL_CARD_UPDATE
)


@dataclass
class HamsterBot:
    storage: Storage
    http_client: HTTPClient
    user: UserModel

    def user_sync(self) -> bool:
        body_http_client = {
            'token': self.user.token,
            'endpoint': URL_INFO_SYNC,
            'proxy': self.user.proxy
        }
        try:
            result_response = self.http_client.post(**body_http_client)
            if result_response == 200:
                return True
        except Exception as e:
            return False
        
    def user_tap(self) -> dict:
        user_info = self.storage.user_storage[0].get('found', {}).get('clickerUser', None) or self.storage.user_storage[0].get('clickerUser', None)
        if user_info is None:
            raise Exception('user_info not found')
        count = user_info['availableTaps'] // user_info['level']
        body_http_client = {
            'token': self.user.token,
            'endpoint': URL_TAP,
            'data': {
                "count": count, 
                "availableTaps": 0, 
                "timestamp": time.time()
            },
            'proxy': self.user.proxy
        }
        try:

            result_response = self.http_client.post(**body_http_client)
            if result_response == 200:
                logger.info(f'\n{"".center(100, "=")}\nПользователь --> {user_info["id"]}\nНатыкал по экрану монет --> {count * user_info["level"]}\n{"".center(100, "=")}')
                return {
                    'userID': user_info['id'][:6],
                    'count': count * user_info['level'],
                    'msg': f'Собрано {count * user_info["level"]} монет! для {user_info["id"][:6]}...'
                }
        except Exception as e:
            return {'Error': f'TOKEN --> {self.user.token}, BAD response --> {e}'}

    def read_file_and_save_storage(
        self
    ):
        with open(f'{self.user.token}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.storage.user_storage.clear()
            self.storage.user_storage.append(data)


@dataclass
class HamsterBotTaskMorse:
    http_client: HTTPClient
    user: UserModel
    morse: MorseHamsterSchema

    def morse_task(self):
        body_http_client = {
            'token': self.user.token,
            'endpoint': URL_MORSE,
            'data': {
                "cipher": self.morse.code, 
            },
            'proxy': self.user.proxy
        }
        try:
            result_response = self.http_client.post(**body_http_client)
            if result_response == 200:
                return {
                    'userID': f'{self.user.token[:8]}...',
                    'msg': f'Отгадал морзянку! для пользователя {self.user.token[:8]}... | +1 000 000'
                }
        except Exception as e:
            return {
                'userID': 'None',
                'msg': f'Не удалось отправить запрос на угадывания морзянки! --> {e}'
            }
        
@dataclass
class HamsterBotTaskCard:
    http_client: HTTPClient
    user: UserModel
    storage: Storage

    def get_my_card(self):
        body_http_client = {
            'token': self.user.token,
            'endpoint': URL_GET_MY_CARD,
            'proxy': self.user.proxy
        }
        try:  
            result_response = self.http_client.post_get_card(**body_http_client)
            if result_response == 200:
                return True
        except Exception as e:
            return {
                'userID': 'None',
                'msg': f'Bad Request get card -> {e}'
            }
        
    def request_card_update(self, id: str):
        body_http_client = {
            'token': self.user.token,
            'endpoint': URL_CARD_UPDATE,
            'proxy': self.user.proxy,
            'data': {
                'upgradeId': id,
                'timestamp': time.time()
            }
        }

        try:
            print(f'ID КАРТЫ  ЗАХОДИТ В ЗАПРОС --> {id}')
            result_response = self.http_client.post(**body_http_client)
            if result_response == 200:
                self.get_my_card()
                return {
                    'userID': self.user.token[:8],
                    'msg': f'Прокачал карту -> {id}'
                }
        except Exception as e:
            print(f'карта не прокачалась | Error --> {e}')

        
    def read_file_card(self) -> Optional[List[CardSchema]]:
        with open(f'card_{self.user.token}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [CardSchema(**i_card) for i_card in data['upgradesForBuy']] if len(data['upgradesForBuy']) > 1 else None

    def card(self):
        user_info = self.storage.user_storage[0].get('found', {}).get('clickerUser', None) or self.storage.user_storage[0].get('clickerUser', None)
        balance = user_info['balanceCoins']
        my_card = self.read_file_card()
        score = 0
        responses = []

        while 15 > score:
            for i_card_update in CARDS_UPDATE:
                for j_my_card in my_card:
                    if i_card_update.id == j_my_card.id\
                    and i_card_update.level > j_my_card.level\
                    and balance > j_my_card.price\
                    and not j_my_card.isExpired\
                    and j_my_card.isAvailable:
                        response = self.request_card_update(j_my_card.id)
                        my_card = self.read_file_card()
                        responses.append(response)
                        score += 1
                    else:
                        continue

        return {'msg': responses}
                        
    def user_sync(self) -> bool:
        body_http_client = {
            'token': self.user.token,
            'endpoint': URL_INFO_SYNC,
            'proxy': self.user.proxy
        }
        try:
            result_response = self.http_client.post(**body_http_client)
            if result_response == 200:
                return True
        except Exception as e:
            return {'msg': f'sync error -> {e}'}
        
    def read_file_and_save_storage(
        self
    ):
        with open(f'{self.user.token}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.storage.user_storage.clear()
            self.storage.user_storage.append(data)


# @dataclass
# class HamsterBotTaskCombo:
#     http_client: HTTPClient
#     user: UserModel