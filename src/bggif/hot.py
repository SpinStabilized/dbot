# -*- coding: utf-8 -*-
"""A module for interacting with BoardGameGeek (BGG) hot games data.

This module provides functionality to retrieve information about hot games from
BoardGameGeek (BGG) using their XML API. It includes a class, HotGame,
representing a hot game on BGG, with methods to retrieve hot games data and
generate BGG URLs.

Classes:
    HotGame: Represents a hot game on BoardGameGeek (BGG), with methods to
             retrieve hot games data and generate BGG URLs.

Variables:
    BASE_URI (str): Base URI for the BoardGameGeek (BGG) XML API.
    SITE_BASE_URL (str): Base URL for BGG game pages.

Example usage:
    if __name__ == '__main__':
        hot_games = await HotGame.get_hot_games()
        for game in hot_games:
            print(game.name, game.rank)
"""
import aiohttp
import xmltodict

BASE_URI = 'https://www.boardgamegeek.com/xmlapi2/'
SITE_BASE_URL = 'https://boardgamegeek.com/boardgame/'


class HotGame:
    """Represents a hot game on BoardGameGeek (BGG) with attributes and methods for interaction.

    Attributes:
        id (int): The unique identifier of the game.
        rank (int): The rank of the game among hot games on BGG.
        thumbnail (str): The URL of the game's thumbnail image.
        name (str): The name of the game.
        year_published (int): The publication year of the game.
    
    Methods:
        get_hot_games(cls): Asynchronously retrieves hot games data from BGG.
        bgg_url: Property that returns the URL of the game on BGG.

    """
    def __init__(self, **kwargs) -> None:
        self.id: int = int(kwargs.get('@id', '0'))
        self.rank: int = int(kwargs.get('@rank', 0))
        self.thumbnail: str = kwargs.get('thumbnail', '').get('@value', '')
        self.name: str = kwargs.get('name', '').get('@value', '')
        self.year_published: int = int(kwargs.get('yearpublished', '0').get('@value', '0'))
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def __repr__(self) -> str:
        return f'<HotGame - {self.name}>'
    
    @classmethod
    async def get_hot_games(cls) -> list:
        """Asynchronously retrieves hot games data from BoardGameGeek (BGG).

        This method sends a request to the BGG API to fetch data about hot
        games. If the request is successful (status code 200), the response is
        parsed as XML. The data is then extracted and used to create HotGame
        objects, which are returned as a list.

        Returns:
            list[HotGame]: A list of HotGame objects representing hot games on BGG.

        Raises:
            None
        """
        params: str = 'hot?boardgame'
        full_bgg_url: str = BASE_URI + params
        game_list: list[HotGame] = None
        async with aiohttp.ClientSession() as session:
            async with session.get(full_bgg_url) as response:
                if response.status == 200:
                    raw_xml: str = await response.text()
                    game_data: dict = xmltodict.parse(raw_xml)['items']['item']
                    game_list = [cls(**i) for i in game_data]
        return game_list

    @property
    def bgg_url(self) -> str:
        """The URL of the game on BoardGameGeek (BGG).

        This property generates and returns the URL of the game on BGG based on
        its unique identifier (id).

        Returns:
            str: The URL of the game on BGG.

        Raises:
            None
        """
        return SITE_BASE_URL + str(self.id) + '/'


if __name__ == '__main__':
    print([g.get_site_url for g in HotGame.get_hot_games()])