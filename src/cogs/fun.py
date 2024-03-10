# -*- coding: utf-8 -*-
import subprocess

from discord.ext import commands

import discord
import utils

logger = utils.get_dbot_logger()

COWSAY = '/usr/games/cowsay'
COWTHINK = '/usr/games/cowthink'
FORTUNE = '/usr/games/fortune'

class FunBot(commands.Cog):
    """Some fun commands."""

    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        logger.info('FunBot Cog Loaded')
    
    @commands.command(aliases=['cs'], help='cowsay [-e eye_string] [-f cowfile] [-l] [-n] [-T tongue_string] [-W column] [-bdgpstwy]')
    async def cowsay(self, ctx, *, message:str='Moo'):
        logger.info(f'\t{message}')
        async with ctx.typing():
            args = message.split(' ')
            data = subprocess.run([COWSAY] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await ctx.send(f'```{data.stdout}```')

    @commands.command(aliases=['ct'], help='cowthink [-e eye_string] [-f cowfile] [-l] [-n] [-T tongue_string] [-W column] [-bdgpstwy]')
    async def cowthink(self, ctx, *, message:str='Moo'):
        logger.info(f'\t{message}')
        async with ctx.typing():
            args = message.split(' ')
            data = subprocess.run([COWTHINK] + args,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT,
                   text=True)
        await ctx.send(f'```{data.stdout}```')

    @commands.command(help='Display a fortune from the famous UNIX command.')
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