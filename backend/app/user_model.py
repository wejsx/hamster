from dataclasses import dataclass

@dataclass
class UserModel:
    token: str
    proxy: dict