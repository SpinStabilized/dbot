# -*- coding: utf-8 -*-
from __future__ import annotations

import aiohttp
import xmltodict

from typing import List

BASE_URI = 'https://www.boardgamegeek.com/xmlapi2/'
SITE_BASE_URL = 'https://boardgamegeek.com/boardgame/'


class HotGame:
    def __init__(self, **kwargs) -> None:
        self.id = int(kwargs.get('@id', '0'))
        self.rank = int(kwargs.get('@rank', 0))
        self.thumbnail = kwargs.get('thumbnail', '').get('@value', '')
        self.name = kwargs.get('name', '').get('@value', '')
        self.year_published = int(kwargs.get('yearpublished', '0').get('@value', '0'))
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def __repr__(self) -> str:
        return f'<HotGame - {self.name}>'
    
    @classmethod
    async def get_hot_games(cls) -> List[HotGame]:
        params = 'hot?boardgame'
        full_bgg_url = BASE_URI + params
        game_list = None
        async with aiohttp.ClientSession() as session:
            async with session.get(full_bgg_url) as response:
                if response.status == 200:
                    raw_xml = await response.text()
                    game_data = xmltodict.parse(raw_xml)['items']['item']
                    game_list = [cls(**i) for i in game_data]
        return game_list

    @property
    def bgg_url(self) -> str:
        return SITE_BASE_URL + str(self.id) + '/'


if __name__ == '__main__':
    print([g.get_site_url for g in HotGame.get_hot_games()])