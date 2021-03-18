# -*- coding: utf-8 -*-
from __future__ import annotations

import discord
import logging

from discord.ext import commands

import bggif.hot

logger = logging.getLogger('dbot')

class BggBot(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        logger.info('BggBot Cog Loaded')
    
    @commands.command(aliases=['bggh'], help='Get the top n games from the BGG Hot list. Default 10, max 50.')
    async def bgg_hot(self, ctx, *, number: int=10) -> None:
        logger.info(f'{ctx.author} requested the top {number} hottest games from BGG')
        hot_games = bggif.hot.HotGame.get_hot_games()
        for game in hot_games[:number]:
            async with ctx.typing():
                hot_embed = as_disc_embed(ctx, game)
            await ctx.reply(embed=hot_embed)


def as_disc_embed(ctx, game) -> discord.Embed:
    hot_embed = discord.Embed(color=discord.Color.light_grey())
    # hot_embed.title = f'#{game.rank} - {game.name} ({game.year_published})'
    hot_embed.set_author(name=f'#{game.rank} - {game.name} ({game.year_published})', icon_url=game.thumbnail, url=game.get_site_url)
    # hot_embed.set_thumbnail(url=game.thumbnail)
    hot_embed.set_footer(text="BGG Hot Boardgames List")
    return hot_embed

def setup(bot: "Bot") -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    bot.add_cog(BggBot(bot))