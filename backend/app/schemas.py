from dataclasses import dataclass
from typing import Union, Dict, Optional

@dataclass
class MorseHamsterSchema:
    code: str

@dataclass
class UsersSchema:
    token: str
    
@dataclass
class CardSchema:
    id: str
    name: str
    price: int
    profitPerHour: int
    condition: Union[Dict[str, Union[str, int]], None]
    section: str
    level: int
    currentProfitPerHour: int
    profitPerHourDelta: int
    isAvailable: bool
    isExpired: bool
    cooldownSeconds: Optional[int] = None
    totalCooldownSeconds: Optional[int] = None
    expiresAt: Optional[str] = None
    maxLevel: Optional[int] = None
    welcomeCoins: Optional[int] = None

@dataclass
class CardUpdateSchema:
    id: str
    level: int