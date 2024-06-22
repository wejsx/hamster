from dataclasses import dataclass
from typing import Union, Dict, Optional

from schemas import CardUpdateSchema


URL_INFO_SYNC = 'https://api.hamsterkombat.io/clicker/sync'
URL_TAP = 'https://api.hamsterkombat.io/clicker/tap'
URL_MORSE = 'https://api.hamsterkombat.io/clicker/claim-daily-cipher'
URL_GET_MY_CARD = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
URL_CARD_UPDATE = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
URL_COMBO = 'https://api.hamsterkombat.io/clicker/claim-daily-combo'

CARDS_UPDATE = [
    CardUpdateSchema(
        id='fan_tokens',
        level=8
    ),
    CardUpdateSchema(
        id='eth_pairs',
        level=10
    ),
    CardUpdateSchema(
        id='btc_pairs',
        level=11
    ),
    CardUpdateSchema(
        id='staking',
        level=11
    ),
    CardUpdateSchema(
        id='licence_asia',
        level=11
    ),
    CardUpdateSchema(
        id='licence_south_america',
        level=11
    ),
    CardUpdateSchema(
        id='kyb',
        level=11
    ),
    CardUpdateSchema(
        id='kyc',
        level=11
    ),
    CardUpdateSchema(
        id='legal_opinion',
        level=11
    ),
    CardUpdateSchema(
        id='top_10_cmc_pairs',
        level=11
    ),
    CardUpdateSchema(
        id='support_team',
        level=11
    ),
    CardUpdateSchema(
        id='x',
        level=11
    ),
    CardUpdateSchema(
        id='medium',
        level=11
    ),
    CardUpdateSchema(
        id='facebook_ads',
        level=11
    ),
    CardUpdateSchema(
        id='shit_coins',
        level=11
    ),
    CardUpdateSchema(
        id='margin_trading_x30',
        level=11
    ),
    CardUpdateSchema(
        id='meme_coins',
        level=11
    ),
    CardUpdateSchema(
        id='influencers',
        level=11
    ),
    CardUpdateSchema(
        id='margin_trading_x10',
        level=11
    ),
    CardUpdateSchema(
        id='margin_trading_x10',
        level=11
    ),
    CardUpdateSchema(
        id='reddit',
        level=11
    ),
    CardUpdateSchema(
        id='youtube',
        level=11
    ),
    CardUpdateSchema(
        id='anti_money_loundering',
        level=11
    ),
    CardUpdateSchema(
        id='licence_uae',
        level=11
    ),
    CardUpdateSchema(
        id='p2p_trading',
        level=11
    ),
    CardUpdateSchema(
        id='margin_trading_x50',
        level=11
    ),
    CardUpdateSchema(
        id='web3_integration',
        level=11
    ),

    
    
    CardUpdateSchema(
        id='licence_europe',
        level=2
    ),
    CardUpdateSchema(
        id='consensys_explorer_pass',
        level=2
    ),
    CardUpdateSchema(
        id='consensys_piranja_pass',
        level=2
    ),
    CardUpdateSchema(
        id='licence_australia',
        level=2
    ),
    CardUpdateSchema(
        id='licence_europe',
        level=2
    ),
    CardUpdateSchema(
        id='web3_academy_launch',
        level=2
    ),
    CardUpdateSchema(
        id='top10_global',
        level=2
    ),
    CardUpdateSchema(
        id='special_hamster_conference',
        level=2
    ),
    CardUpdateSchema(
        id='apps_center_listing',
        level=2
    ),
]


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