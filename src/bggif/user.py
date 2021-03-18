# -*- coding: utf-8 -*-
from __future__ import annotations


import requests
import xmltodict

from datetime import date, timedelta
from typing import List

BASE_URI = 'https://www.boardgamegeek.com/xmlapi2/'
SITE_BASE_URL = 'https://boardgamegeek.com/user/'

class User:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get('@id', '')
        self.id = int(self.id) if self.id != '' else 0
        self.name = kwargs.get('@name', '')
        self.first_name = kwargs.get('firstname', '').get('@value', '')
        self.last_name = kwargs.get('lastname', '').get('@value', '')
        self.avatar = kwargs.get('avatarlink', '').get('@value', '')
        self.year_registered = kwargs.get('yearregistered', '').get('@value', '')
        self.last_login = kwargs.get('lastlogin', '').get('@value', '')
        if self.last_login:
            self.last_login = date.fromisoformat(self.last_login)
        self.state_or_province = kwargs.get('stateorprovince', '').get('@value', '')
        self.country = kwargs.get('country', '').get('@value', '')
        self.web_address = kwargs.get('webaddress', '').get('@value', '')
        self.xbox_account = kwargs.get('xboxaccount', '').get('@value', '')
        self.wii_account = kwargs.get('wiiaccount', '').get('@value', '')
        self.psn_addount = kwargs.get('psnaccount', '').get('@value', '')
        self.battle_net_account = kwargs.get('battlenetaccount', '').get('@value', '')
        self.steam_account = kwargs.get('steamaccount', '').get('@value', '')
        self.trade_rating = int(kwargs.get('traderating', '0').get('@value', '0'))
        self.market_rating = int(kwargs.get('marketrating', '0').get('@value', '0'))
        
    
    @classmethod
    def get_user(self, username: str='') -> List[User]:
        uri = BASE_URI + 'user'
        parameters = {'name':username}
        response = requests.get(uri, params=parameters)
        user = None
        if response.status_code == 200:
            user = User(**xmltodict.parse(response.text)['user'])
        return user
    
    @property
    def valid(self) -> bool:
        return True if self.id != 0 else False
    
    @property
    def bgg_url(self) -> str:
        return SITE_BASE_URL + self.name
    
    @property
    def login_delta(self) -> int:
        time_since = date.today() - self.last_login
        return time_since.days

if __name__ == '__main__':
    user = User.get_user('scifilaura')
    print(user.first_name, user.last_name, user.last_login, user.market_rating)