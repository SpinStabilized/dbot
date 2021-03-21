# -*- coding: utf-8 -*-
import discord
import logging
import subprocess

from discord.ext import commands

logger = logging.getLogger('dbot')

COWSAY = '/usr/games/cowsay'
COWTHINK = '/usr/games/cowthink'
FORTUNE = '/usr/games/fortune'

class FunBot(commands.Cog):

    def __init__(self, bot:'Bot') -> None:
        self.bot = bot
        logger.info('FunBot Cog Loaded')
    
    @commands.command(aliases=['cs'], help='cowsay [-e eye_string] [-f cowfile] [-l] [-n] [-T tongue_string] [-W column] [-bdgpstwy]')
    async def cowsay(self, ctx, *, message:str='Moo'):
        async with ctx.typing():
            args = message.split(' ')
            data = subprocess.run([COWSAY] + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        await ctx.send(f'```{data.stdout}```')

    @commands.command(aliases=['ct'], help='cowthink [-e eye_string] [-f cowfile] [-l] [-n] [-T tongue_string] [-W column] [-bdgpstwy]')
    async def cowthink(self, ctx, *, message:str='Moo'):
        async with ctx.typing():
            args = message.split(' ')
            data = subprocess.run([COWTHINK] + args,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT,
                   text=True)
        await ctx.send(f'```{data.stdout}```')

    @commands.command(help='fortune [-afilosw] [-m pattern] [-n number]')
    async def fortune(self, ctx, *, ignore:None=None):
        async with ctx.typing():
            data = subprocess.run([FORTUNE], 
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT,
                   text=True)
        await ctx.send(f'```{data.stdout}```')


def setup(bot: "Bot") -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    bot.add_cog(FunBot(bot))