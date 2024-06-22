from schemas import MorseHamsterSchema
from storage_model import Storage
from user_model import UserModel
from http_client import HTTPClient
from hamster import HamsterBot, HamsterBotTaskMorse, HamsterBotTaskCard

class HamsterService:
    def __init__(
        self, 
        storage: Storage,
        http_client: HTTPClient, 
        user: UserModel
    ) -> None:
        self.bot = HamsterBot(storage, http_client, user)

    def proccess(self):
        self.bot.user_sync()
        self.bot.read_file_and_save_storage()
        return self.bot.user_tap()

class HamsterBotTaskMorseService:
    def __init__(
        self,
        http_client: HTTPClient,
        user: UserModel,
        morse: MorseHamsterSchema
    ) -> None:
        self.bot = HamsterBotTaskMorse(http_client, user, morse)

    def morse_run(self):
        return self.bot.morse_task()
    
class HamsterBotTaskCardService:
    def __init__(
        self,
        http_client: HTTPClient,
        user: UserModel,
        storage: Storage
    ) -> None:
        self.bot = HamsterBotTaskCard(http_client, user, storage)

    def process(self):
        self.bot.user_sync()
        self.bot.read_file_and_save_storage()
        self.bot.get_my_card()
        return self.bot.card()