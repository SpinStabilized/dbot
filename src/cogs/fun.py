# -*- coding: utf-8 -*-
import subprocess
import os

from discord.ext import commands

import discord
import utils

logger = utils.get_dbot_logger()

PREFIX = os.getenv('DISCORD_BOT_PREFIX')

COWSAY_WHICH = subprocess.run(['which', 'cowsay'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
COWTHINK_WHICH = subprocess.run(['which', 'cowthink'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
FORTUNE_WHICH = subprocess.run(['which', 'fortune'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

COWSAY = COWSAY_WHICH.stdout.strip()
COWTHINK = COWTHINK_WHICH.stdout.strip()
FORTUNE = FORTUNE_WHICH.stdout.strip()

FUN_COWSAY_HELP_BRIEF = 'The cow says "Moo" or whatever you want.'
FUN_COWSAY_HELP_LONG = f"""
{FUN_COWSAY_HELP_BRIEF}

Example:
\t>{PREFIX}cowsay "DBot Rocks!"

\t _______________ 
\t< "DBot Rocks!" >
\t --------------- 
\t        \\   ^__^
\t         \\  (oo)\\_______
\t            (__)\\       )\\/\\
\t                ||----w |
\t                ||     ||
"""

FUN_COWTHINK_HELP_BRIEF = 'The cow thinks "Moo" or whatever you want.'
FUN_COWTHINK_HELP_LONG = f"""
{FUN_COWTHINK_HELP_BRIEF}

Example:
\t>{PREFIX}cowthink "DBot Rocks!"

\t _______________ 
\t( "DBot Rocks!" )
\t --------------- 
\t        o   ^__^
\t         o  (oo)\\_______
\t            (__)\\       )\\/\\
\t                ||----w |
\t                ||     ||
"""

FUN_FORTUNE_HELP_BRIEF = 'Display a fortune from the famous UNIX command.'
FUN_FORTUNE_HELP_LONG = f"""
{FUN_FORTUNE_HELP_BRIEF}

Example:
\t>{PREFIX}fortune
\t"Hello again, Peabody here..."
\t-- Mister Peabody
"""

class FunBot(commands.Cog, name='Some additional "fun"ctionality.'):
    """Some fun commands."""

    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        logger.info('FunBot Cog Loaded')
    
    @commands.command(
            aliases=['cs'],
            brief=FUN_COWSAY_HELP_BRIEF,
            help=FUN_COWSAY_HELP_LONG,
    )
    async def cowsay(self, ctx, *, message:str = commands.parameter(default='Moo', description='Message for the cow to say.')):
        logger.info(f'\t{message}')
        async with ctx.typing():
            args = message.split(' ')
            data = subprocess.run([COWSAY] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await ctx.send(f'```{data.stdout}```')

    @commands.command(
            aliases=['ct'],
            brief=FUN_COWTHINK_HELP_BRIEF,
            help=FUN_COWTHINK_HELP_LONG,
    )
    async def cowthink(self, ctx, *, message:str = commands.parameter(default='Moo', description='Message for the cow to think.')):
        logger.info(f'\t{message}')
        async with ctx.typing():
            args = message.split(' ')
            data = subprocess.run([COWTHINK] + args,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT,
                   text=True)
        await ctx.send(f'```{data.stdout}```')

    @commands.command(
            brief=FUN_FORTUNE_HELP_BRIEF,
            help=FUN_FORTUNE_HELP_LONG,
    )
    async def fortune(self, ctx):
        async with ctx.typing():
            data = subprocess.run([FORTUNE], 
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT,
                   text=True)
            em = discord.Embed(color=discord.Color.light_grey())
            em.title = f'Fortune'
            em.description = data.stdout
        # await ctx.send(f'{data.stdout}')
        await ctx.send(embed=em)


async def setup(bot: commands.Bot) -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    await bot.add_cog(FunBot(bot))