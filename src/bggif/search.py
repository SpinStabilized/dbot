# -*- coding: utf-8 -*-
"""A module for interacting with search results from BoardGameGeek (BGG) API.

This module provides functionality to perform search queries on BoardGameGeek
(BGG) and retrieve search results.

It includes a class, SearchItem, representing an item obtained from a search
query on BGG, with methods to perform searches and generate BGG URLs.

Classes:
    SearchItem: Represents an item obtained from a search query on BGG, with
                methods to perform searches and generate BGG URLs.

Variables:
    BASE_URI (str): Base URI for the BoardGameGeek (BGG) XML API.
    SITE_BASE_URL (str): Base URL for BGG game pages.

Example usage:
    search_results = await SearchItem.search('Catan')
    for item in search_results:
        print(item.name, item.bgg_url)
"""

import aiohttp
import xmltodict
from typing import TypeVar

BASE_URI = 'https://www.boardgamegeek.com/xmlapi2/'
SITE_BASE_URL = 'https://boardgamegeek.com/boardgame/'


SearchItem_Type =  TypeVar('SearchItem_Type', bound='SearchItem')
class SearchItem:
    """Represents an item obtained from a search query on BoardGameGeek (BGG).

    Attributes:
        id (int): The unique identifier of the item.
        name (str): The name of the item.
        year_published (int): The publication year of the item, if available.

    Methods:
        search: Asynchronously searches BGG for items matching the specified query.
        bgg_url: Property that returns the URL of the item on BGG.

    Example usage:
        search_results = await SearchItem.search('Catan')
        for item in search_results:
            print(item.name, item.bgg_url)
    """

    def __init__(self, **kwargs) -> None:
        print(kwargs)
        self.id = int(kwargs.get('@id', '0'))
        self.name = kwargs.get('name', '').get('@value', '')
        self.year_published = None
        if 'yearpublished' in kwargs.keys():
            self.year_published = int(kwargs['yearpublished'].get('@value', '0'))
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def __repr__(self) -> str:
        return f'<Item - {self.name}>'
    
    @classmethod
    async def search(cls, search_str: str='') -> list[SearchItem_Type]:
        """Asynchronously searches BoardGameGeek (BGG) for games matching the specified query.

        This method sends a request to the BGG API to search for games based on
        the provided search string. The search string is cleaned and formatted
        before being used as a query parameter in the API request.
        
        If the request is successful (status code 200), the response is parsed
        as XML. The search results are extracted and filtered to include only
        items with publication year information.
        
        If there are more than 10 results, only the first 10 are returned.
        
        The search results are then converted into SearchItem objects and
        returned as a list.

        Parameters:
            search_str (str, optional): The search query string. Defaults to an empty string.

        Returns:
            list[SearchItem]: A list of SearchItem objects representing search results from BGG.

        Raises:
            None
        """
        cleaned_search: str = search_str.replace(' ', '+')
        uri: str = BASE_URI + 'search'
        parameters: dict[str, str] = {'query':cleaned_search}
        results: list[SearchItem] = []
        async with aiohttp.ClientSession() as session:
            async with session.get(uri, params=parameters) as response:
                if response.status == 200:
                    raw_xml = await response.text()
                    results = xmltodict.parse(raw_xml)['items'].get('item', None)
                    results = [result for result in results if 'yearpublished' in result.keys()]
                    if results and len(results) > 10:
                        results = results[:10]
                    if results:
                        results = [SearchItem(**result) for result in results]
        return results

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


