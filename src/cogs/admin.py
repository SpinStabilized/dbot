# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import discord
import os
import platform

from discord.ext import commands

import utils

logger = utils.get_dbot_logger()

PREFIX = os.getenv('DISCORD_BOT_PREFIX')

ADMIN_ABOUT_HELP_BRIEF = 'About DBot'
ADMIN_ABOUT_HELP_LONG = f"""
{ADMIN_ABOUT_HELP_BRIEF}

Example:
\t>{PREFIX}about

"""

ADMIN_CALC_HELP_BRIEF = 'A handy calculator'
ADMIN_CALC_HELP_LONG = f"""
{ADMIN_CALC_HELP_BRIEF}

A calculator that takes in a math expression and returns the result.

Example:
\t>dbot calc 1+1
\t> 2

\t>{PREFIX}calc cos(pi)
\t>-1.0

"""

ADMIN_PING_HELP_BRIEF = 'Report the response latency to the bot in ms.'
ADMIN_PING_HELP_LONG = f"""
{ADMIN_PING_HELP_BRIEF}

Example:
\t>{PREFIX}ping

"""

ADMIN_UPTIME_HELP_BRIEF = 'The amount of time since DBot was started.'
ADMIN_UPTIME_HELP_LONG = f"""
{ADMIN_UPTIME_HELP_BRIEF}

Example:
\t>{PREFIX}uptime

"""

class BotAdmin(commands.Cog, name='DBot Administration Functions'):
    """Administrative Commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        logger.info('BotAdmin Cog Loaded')
        self.start_time = datetime.datetime.now()

    @commands.command(
            brief=ADMIN_ABOUT_HELP_BRIEF,
            help=ADMIN_ABOUT_HELP_LONG,
    )
    async def about(self, ctx) -> None:
        up = self.start_time - datetime.datetime.now()
        async with ctx.typing():
            '''Shows info about bot'''
            em = discord.Embed(color=discord.Color.green())
            em.title = 'About DBot'
            em.set_author(name=ctx.author.name, icon_url=ctx.author.default_avatar)
            em.description = f'The DBot'
            em.add_field(name='Servers', value=len(self.bot.guilds))
            em.add_field(name='Bot Latency', value=f"{self.bot.ws.latency * 1000:.0f} ms")
            em.add_field(name='Up Time', value=str(datetime.datetime.now() - self.start_time))
            em.add_field(name='GitHub', value=f'[Source Repository](https://github.com/SpinStabilized/dbot)')
            em.add_field(name='Invite Me', 
                         value=f'[Click Here](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=1082332280896)')

            em.add_field(name='discord.py Version', value=f'{discord.__version__}')
            em.add_field(name='Python Version', value=f'{platform.python_version()}')
            em.add_field(name='Environment', value=f'{platform.system()} {platform.release()} ({os.name})')
            em.set_footer(text="DBot is powered by discord.py")
        await ctx.send(embed=em)

    @commands.command(
            brief=ADMIN_CALC_HELP_BRIEF,
            help=ADMIN_CALC_HELP_LONG,
    )
    async def calc(self, ctx, calculation: str = commands.parameter(default='0', description='Math expression')):
        logger.info(f'\t{calculation}')
        async with ctx.typing():
            try:
                result = utils.eval_expr(calculation)
                result = f'Results: {result}'
            except SyntaxError as se:
                result = '```Syntax Error In Expression\n'
                result += f'\t{se.text}\n'
                result += f'\t{" " * (se.offset-1)}^```'
        await ctx.reply(result)

    @commands.command(hidden=True)
    @utils.dev_only()
    async def log_get(self, ctx):
        await ctx.reply(file=discord.File(str(utils.DBOT_LOG_FILE)))

    @commands.command(hidden=True)
    @utils.dev_only()
    async def log_tail(self, ctx, n: int = 10):
        logger.info(f'\t{n} lines of the logfile requested')
        log_lines = ''
        with open(utils.DBOT_LOG_FILE, 'r') as log:
            log_lines = ''.join(log.readlines()[-n:])
        await ctx.reply(f'```{log_lines}```')

    @commands.command(
            brief=ADMIN_PING_HELP_BRIEF,
            help=ADMIN_PING_HELP_LONG,
    )
    async def ping(self, ctx):
        async with ctx.typing():
            em = discord.Embed(color=discord.Color.green())
            em.title = "Ping Response"
            em.description = f'{self.bot.latency * 1000:0.2f} ms'
        await ctx.send(embed=em)

    @commands.command(aliases=['sd'], hidden=True)
    @utils.dev_only()
    async def shutdown(self, ctx) -> None:
        logger.warning(f'Providing most recent log before shutdown.')
        await ctx.send(f"DBot is shutting down at {ctx.author}'s request.")
        await ctx.send(f'Providing most recent log before shutdown.')
        await ctx.send(file=discord.File(str(utils.DBOT_LOG_FILE)))
        await self.bot.change_presence(activity=None, status=discord.Status.offline)
        
        await self.bot.close()

    @commands.command(
            brief=ADMIN_UPTIME_HELP_BRIEF,
            help=ADMIN_UPTIME_HELP_LONG,
    )
    async def uptime(self, ctx) -> None:
        up = self.start_time - datetime.datetime.now()
        async with ctx.typing():
            '''Current bot instance uptime'''
            em = discord.Embed(color=discord.Color.green())
            em.title = 'DBot Uptime'
            em.description = str(datetime.datetime.now() - self.start_time)
            em.set_footer(text="DBot is powered by discord.py")
        await ctx.send(embed=em)


async def setup(bot: commands.Bot) -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    await bot.add_cog(BotAdmin(bot))