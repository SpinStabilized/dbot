# -*- coding: utf-8 -*-
"""Provides a class to represent a user on BoardGameGeek (BGG) with associated information.

This module defines the User class, which represents a user on BGG. It includes
attributes for various user details such as ID, username, name, avatar, location,
and ratings. Additionally, it provides methods to retrieve user information from
the BGG API and properties to access user-related URLs and calculated attributes.

Example usage:
    user_info = await User.get_user('username')
    print(user_info.full_name)
    print(user_info.location)
"""

import aiohttp
import datetime
import xmltodict
import yarl

from typing import TypeVar

BASE_URI = 'https://www.boardgamegeek.com/xmlapi2/'
SITE_BASE_URL = 'https://boardgamegeek.com/boardgame/'

User_Type =  TypeVar('User_Type', bound='User')
class User:
    """Represents a user on BoardGameGeek (BGG) with associated information.

    Attributes:
        id (int): The unique identifier of the user.
        name (str): The username of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        avatar (str): The avatar link of the user.
        year_registered (str): The year when the user registered on BGG.
        last_login (str): The last login date of the user.
        state_or_province (str): The state or province of the user's location.
        country (str): The country of the user's location.
        web_address (str): The web address of the user.
        xbox_account (str): The Xbox account name of the user.
        wii_account (str): The Wii account name of the user.
        psn_addount (str): The PlayStation Network account name of the user.
        battle_net_account (str): The Battle.net account name of the user.
        steam_account (str): The Steam account name of the user.
        trade_rating (int): The trade rating of the user.
    
    Methods:
        get_user: Asynchronously retrieves user information from the BGG API.
    
    Properties:
        valid: Determines if the user is valid.
        bgg_url: Generates the URL of the user's profile on BGG.
        login_delta: Calculates the number of days since the user's last login.
        full_name: Returns the full name of the user.
        location: Returns the location of the user.

    Example usage:
        user_info = await User.get_user('username')
        print(user_info.full_name)
        print(user_info.location)
    """
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get('@id', '')
        self.id = int(self.id) if self.id != '' else 0
        self.name = kwargs.get('@name', '')
        self.first_name = kwargs.get('firstname', '').get('@value', '')
        self.last_name = kwargs.get('lastname', '').get('@value', '')
        self.avatar = kwargs.get('avatarlink', '').get('@value', '')
        if self.avatar == 'N/A':
            self.avatar = ''
        self.year_registered = kwargs.get('yearregistered', '').get('@value', '')
        self.last_login = kwargs.get('lastlogin', '').get('@value', '')
        if self.last_login:
            self.last_login = datetime.date.fromisoformat(self.last_login)
        self.state_or_province = kwargs.get('stateorprovince', '').get('@value', '')
        self.country = kwargs.get('country', '').get('@value', '')
        self.web_address = kwargs.get('webaddress', '').get('@value', '')
        self.xbox_account = kwargs.get('xboxaccount', '').get('@value', '')
        self.wii_account = kwargs.get('wiiaccount', '').get('@value', '')
        self.psn_addount = kwargs.get('psnaccount', '').get('@value', '')
        self.battle_net_account = kwargs.get('battlenetaccount', '').get('@value', '')
        self.steam_account = kwargs.get('steamaccount', '').get('@value', '')
        self.trade_rating = int(kwargs.get('traderating', '0').get('@value', '0'))
        # self.market_rating = int(kwargs.get('marketrating', '0').get('@value', '0'))
        
    
    @classmethod
    async def get_user(self, username: str='') -> User_Type:
        """Asynchronously retrieves user information from BoardGameGeek (BGG) API.

        This method sends a request to the BGG API to retrieve information about
        a user based on the provided username. The username is used as a query
        parameter in the API request.

        If the request is successful (status code 200), the response is parsed
        as XML. The user information is extracted from the XML response and used
        to initialize a User object.

        Parameters:
            username (str, optional): The username of the BGG user. Defaults to an empty string.

        Returns:
            User: Information on a BGG user represented as User objects.

        Raises:
            None
        """
        uri: str = BASE_URI + 'user'
        parameters: dict[str, str] = {'name':username}
        user: User = None
        async with aiohttp.ClientSession() as session:
            async with session.get(uri, params=parameters) as response:
                if response.status == 200:
                    raw_xml = await response.text()
                    user = User(**xmltodict.parse(raw_xml)['user'])
        return user
    
    @property
    def valid(self) -> bool:
        """Determines if the user is valid.

        Returns:
            bool: True if the user has a valid ID, False otherwise.
        """
        return True if self.id != 0 else False
    
    @property
    def bgg_url(self) -> str:
        """Generates the URL of the user's profile on BoardGameGeek (BGG).

        Returns:
            str: The URL of the user's profile on BGG.
        """
        user_uri: str = str(yarl.URL(self.name))
        return SITE_BASE_URL + user_uri
    
    @property
    def login_delta(self) -> int:
        """Calculates the number of days since the user's last login.

        Returns:
            int: The number of days since the user's last login if the user is
                 valid and the last login date is available, otherwise -1.
        """
        if self.valid and self.last_login != '':
            time_since: datetime.timedelta = datetime.date.today() - self.last_login
            return time_since.days
        else:
            return -1
        
    @property
    def full_name(self) -> str:
        """Returns the full name of the user.

        Returns:
            str: The full name of the user.
        """
        return f'{self.first_name} {self.last_name}'
    
    @property
    def location(self) -> str:
        """Returns the location of the user.

        Returns:
            str: The location of the user, formatted as 'state_or_province, country'.
        """
        return f'{self.state_or_province}, {self.country}'

if __name__ == '__main__':
    user = User.get_user('scifilaura')
    print(user.first_name, user.last_name, user.last_login, user.market_rating)