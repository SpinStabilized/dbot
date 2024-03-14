# -*- coding: utf-8 -*-
from __future__ import annotations

import aiohttp
import xmltodict

from typing import List

BASE_URI = 'https://www.boardgamegeek.com/xmlapi2/'
SITE_BASE_URL = 'https://boardgamegeek.com/boardgame/'


class SearchItem:
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
    async def search(self, search_str: str='') -> List[SearchItem]:
        cleaned_search: str = search_str.replace(' ', '+')
        uri = BASE_URI + 'search'
        parameters = {'query':cleaned_search}
        results = []
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
        return SITE_BASE_URL + str(self.id) + '/'


