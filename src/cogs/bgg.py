# -*- coding: utf-8 -*-
"""Some functions that interface to the Board Game Geek API.

"""

import discord
import logging
import os

from discord.ext import commands

import bggif.hot
import bggif.search
import bggif.user
import utils

logger: logging.Logger = utils.get_dbot_logger()

PREFIX: str = os.getenv('DISCORD_BOT_PREFIX')

################################################################################
# Help Documentation
################################################################################

#######################################
# bgg_hot command help
#######################################
BGG_HOT_HELP_BRIEF = 'Get the top n games from the BGG Hot list. Default 10, max 50.'
BGG_HOT_HELP_LONG = f"""
{BGG_HOT_HELP_BRIEF}

Retrieve the top games from BGG where number is the number
of games to check. The default is 10 games and the maximum
is 50.

Example:
\t>{PREFIX}bgg_hot
\tDisplay the top 10 games on BGG.

\t>{PREFIX}bgg_hot 1
\tDisplay the current #1 game on BGG.
"""

#######################################
# bgg_search command help
#######################################
BGG_SEARCH_HELP_BRIEF = 'Search for the specified games on BGG.'
BGG_SEARCH_HELP_LONG = f"""
{BGG_SEARCH_HELP_BRIEF}

Example:
\t>{PREFIX}bgg_search Pathfinder
\tReturns up to 10 results associated with the search for Pathfinder

"""

#######################################
# bgg_user command help
#######################################
BGG_USER_HELP_BRIEF = 'Search for the specified user on BGG.'
BGG_USER_HELP_LONG = f"""
{BGG_USER_HELP_BRIEF}

Example:
\t>{PREFIX}bgg_user bjmclaughlin
\tReturns information on the BGG user specified.

"""
class BggBot(commands.Cog, name='Board Game Geek Functions'):
    """Board Game Geek Commands"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        logger.info('BggBot Cog Loaded')
    
    @commands.command(
            aliases=['bggh'],
            brief=BGG_HOT_HELP_BRIEF,
            help=BGG_HOT_HELP_LONG,
    )
    async def bgg_hot(self, ctx: commands.Context, *, 
            number: int = commands.parameter(default=10, description='Number of top games to retrieve.')) -> None:
        """Retrieves and displays the top BoardGameGeek (BGG) hot games.

        This command retrieves the top hot games from BoardGameGeek (BGG) and
        displays them as embedded messages in the Discord channel. The number of
        top games to retrieve can be specified, with a default of 10 if not
        provided.

        Parameters:
            ctx (commands.Context): The context object representing the invocation context.
            number (int, optional): Number of top games to retrieve. Defaults to 10.

        Returns:
            None

        Raises:
            None
        """
        logger.info(f'\tTop {number} games requested.')
        embed_list: list[discord.Embed] = []
        async with ctx.typing():
            hot_games: list[bggif.hot.HotGame] = await bggif.hot.HotGame.get_hot_games()
            for game in hot_games[:number]:
                embed_list.append(hot_embed(ctx, game))
        for e in embed_list:
            await ctx.reply(embed=e)

    @commands.command(
            brief=BGG_SEARCH_HELP_BRIEF,
            help=BGG_SEARCH_HELP_LONG,        
        )
    async def bgg_search(self, ctx: commands.Context,
            *search_string: tuple[str]
        ) -> None:
        """Searches BoardGameGeek (BGG) for the specified query and displays the search results.

        This command performs a search on BoardGameGeek (BGG) based on the
        provided search query and displays the search results as embedded
        messages in the Discord channel. The search query can include multiple
        terms, which are joined together and used to perform the search.

        Parameters:
            ctx (commands.Context): The context object representing the invocation context.
            *search_string (tuple[str]): The search query terms.

        Returns:
            None

        Raises:
            None
        """
        logger.info(f'\tBGG Search on {search_string}')
        joined_search: str = '+'.join(search_string)
        logger.info(joined_search)
        items = None
        async with ctx.typing():
            items: list[bggif.search.SearchItem] = await bggif.search.SearchItem.search(joined_search)
        await ctx.reply(embed=search_item_embed(ctx, items))

    @commands.command(
            aliases=['bggu'],
            brief=BGG_USER_HELP_BRIEF,
            help=BGG_USER_HELP_LONG,        
        )
    async def bgg_user(self, ctx: commands.Context, *,
            username: str = commands.parameter(default='', description='BGG Username')) -> None:
        """Retrieves and displays information about a BoardGameGeek (BGG) user.

        This command retrieves information about a specified BGG user and
        displays it as an embedded message in the Discord channel. The BGG
        username of the user to retrieve information about can be provided as a
        parameter.

        Parameters:
            ctx (commands.Context): The context object representing the invocation context.
            username (str, optional): The BoardGameGeek (BGG) username of the user to retrieve information about. Defaults to an empty string.

        Returns:
            None

        Raises:
            None
        """
        logger.info(f'\tSearching for {username}')
        async with ctx.typing():
            user: bggif.user.User = await bggif.user.User.get_user(username)
            user_info: discord.Embed = user_embed(ctx, user)
        await ctx.reply(embed=user_info)

def search_item_embed(ctx: commands.Context,
        search_items: list[bggif.search.SearchItem]) -> discord.Embed:
    """Generates an embedded message displaying search results from BoardGameGeek (BGG).

    This function takes a list of search items retrieved from a BGG search and
    generates an embedded message displaying the search results. Each search
    item is formatted with its name, publication year (if available), and a
    hyperlink to its corresponding BGG page.

    Parameters:
        ctx (commands.Context): The context object representing the invocation context.
        search_items (list[bggif.search.SearchItem]): A list of search items retrieved from a BGG search.

    Returns:
        discord.Embed: An embedded message displaying the search results.

    Raises:
        None
    """
    search_embed: discord.Embed = discord.Embed(color=discord.Color.light_grey())
    search_embed.title = f'BGG Search Results'
    if search_items:
        for i, item in enumerate(search_items):
            year_published_string: str = f' - ©{item.year_published}' if item.year_published else ''
            search_embed.add_field(
                name=f'{i+1:02})',
                value=f'[{item.name}]({item.bgg_url}){year_published_string}',
                inline=False
            )
    else:
        search_embed.description('No Results')
    return search_embed

def user_embed(ctx: commands.Context, user:bggif.user.User) -> discord.Embed:
    """Generates an embedded message displaying information about a BoardGameGeek (BGG) user.

    This function takes a BGG user object and generates an embedded message
    displaying various details about the user. If the user is not valid (e.g.,
    the user does not exist), a red-colored embedded message indicating the user
    is invalid is generated. Otherwise, a light-grey colored embedded message
    containing information about the user is created.

    Parameters:
        ctx (commands.Context): The context object representing the invocation context.
        user (bggif.user.User): The BoardGameGeek (BGG) user object containing information about the user.

    Returns:
        discord.Embed: An embedded message displaying information about the BGG user.

    Raises:
        None
    """
    user_embed: discord.Embed = None
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

def hot_embed(ctx: commands.Context, game: bggif.hot.HotGame) -> discord.Embed:
    """Generates an embedded message displaying information about a hot BoardGameGeek (BGG) game.

    This function takes a hot BGG game object and generates an embedded message
    displaying details about the game. The embedded message includes the game's
    rank, name, publication year, BGG URL, and a footer indicating the source of
    the information.

    Parameters:
        ctx (commands.Context): The context object representing the invocation context.
        game (bggif.hot.HotGame): The hot BGG game object containing information about the game.

    Returns:
        discord.Embed: An embedded message displaying information about the hot BGG game.

    Raises:
        None
    """
    hot_embed: discord.Embed = discord.Embed(color=discord.Color.light_grey())
    hot_embed.set_author(name=f'#{game.rank} - {game.name} ({game.year_published})', icon_url=game.thumbnail)
    hot_embed.add_field(name='BGG URL', value=f'[{game.name} on BGG]({game.bgg_url})')
    hot_embed.set_footer(text="BGG The Hotness Boardgames List")
    return hot_embed

async def setup(bot: commands.Bot) -> None:
    """Add this Cog to the identified Bot.

    Parameters
    ----------
    bot (commands.Bot): The Bot that this Cog will be added to.
    
    """
    await bot.add_cog(BggBot(bot))