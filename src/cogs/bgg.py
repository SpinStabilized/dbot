# -*- coding: utf-8 -*-
from __future__ import annotations

import discord
import logging

from discord.ext import commands

import bggif.hot
import bggif.user

logger = logging.getLogger('dbot')

class BggBot(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        logger.info('BggBot Cog Loaded')
    
    @commands.command(aliases=['bggh'], help='Get the top n games from the BGG Hot list. Default 10, max 50.')
    async def bgg_hot(self, ctx, *, number: int=10) -> None:
        logger.info(f'{ctx.author} requested the top {number} hottest games from BGG')
        embed_list = []
        async with ctx.typing():
            hot_games = await bggif.hot.HotGame.get_hot_games()
            for game in hot_games[:number]:
                embed_list.append(hot_embed(ctx, game))
        for e in embed_list:
            await ctx.reply(embed=e)

    @commands.command(aliases=['bggu'], help='Get info on a BGG user.')
    async def bgg_user(self, ctx, *, username: str='') -> None:
        logger.info(f'{ctx.author} requested info on BGG user {username}.')
        async with ctx.typing():
            user = await bggif.user.User.get_user(username)
            user_info = user_embed(ctx, user)
        
        await ctx.reply(embed=user_info)

def user_embed(ctx, user:bggif.user.User) -> discord.Embed:
    user_embed = None
    if not user.valid:
        user_embed = discord.Embed(color=discord.Color.red())
        user_embed.title = f'BGG User Lookup: {user.name} - Not A Valid User'
    else:
        user_embed = discord.Embed(color=discord.Color.light_grey())
        user_embed.title = f'BGG User Information'
        if user.avatar:
            user_embed.set_author(name=user.name, icon_url=user.avatar)
        else:
            user_embed.set_author(name=user.name)
        user_embed.add_field(name='BGG Homepage', value=f"[{user.name}'s BGG Homepage]({user.bgg_url})", inline=False)
        if user.full_name != ' ':
            user_embed.add_field(name='Full Name', value=user.full_name)
        user_embed.add_field(name='Year Registered', value=user.year_registered)
        if user.login_delta != -1:
            user_embed.add_field(name='Days Since Last Login', value=user.login_delta)
        if user.location != ', ':
            user_embed.add_field(name='Location', value=user.location, inline=False)
    return user_embed

def hot_embed(ctx, game) -> discord.Embed:
    hot_embed = discord.Embed(color=discord.Color.light_grey())
    # hot_embed.title = f'#{game.rank} - {game.name} ({game.year_published})'
    hot_embed.set_author(name=f'#{game.rank} - {game.name} ({game.year_published})', icon_url=game.thumbnail)
    hot_embed.add_field(name='BGG URL', value=f'[{game.name} on BGG]({game.bgg_url})')
    # hot_embed.set_thumbnail(url=game.thumbnail)
    hot_embed.set_footer(text="BGG The Hotness Boardgames List")
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