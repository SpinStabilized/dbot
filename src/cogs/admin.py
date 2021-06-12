# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import discord

from discord.ext import commands

import utils

logger = utils.get_dbot_logger()

class BotAdmin(commands.Cog):
    """Administrative Commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        logger.info('BotAdmin Cog Loaded')
        self.start_time = datetime.datetime.now()
    
    @commands.command(name='about', help='About DBot')
    async def about(self, ctx) -> None:
        up = self.start_time - datetime.datetime.now()
        async with ctx.typing():
            '''Shows info about bot'''
            em = discord.Embed(color=discord.Color.green())
            em.title = 'About DBot'
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            em.description = 'The DBot'
            em.add_field(name='Servers', value=len(self.bot.guilds))
            em.add_field(name='Bot Latency', value=f"{self.bot.ws.latency * 1000:.0f} ms")
            em.add_field(name='Up Time', value=str(datetime.datetime.now() - self.start_time))
            em.add_field(name='GitHub', value=f'[Source Repository](https://github.com/SpinStabilized/dbot)')
            em.add_field(name='Invite Me', 
                         value=f'[Click Here](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=268905542)')

            em.set_footer(text="DBot is powered by discord.py")
        await ctx.send(embed=em)

    @commands.command(help='Advanced Help')
    async def advanced_help(self, ctx):
        em = discord.Embed(color=discord.Color.dark_gold())
        em.title = "Advanced Help"
        em.description = f'For more help information [visit the help homepage](https://spinstabilized.github.io/dbot-ref/dbot-ref/).'
        await ctx.send(embed=em)

    @commands.command(help='A handy calculator.')
    async def calc(self, ctx, calculation):
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
        logger.info(f'Log file requested by authorized user {ctx.author}')
        await ctx.reply(file=discord.File(str(utils.DBOT_LOG_FILE)))

    @commands.command(hidden=True)
    @utils.dev_only()
    async def log_tail(self, ctx, n: int = 10):
        logger.info(f'Log tail of {n} lines requested by authorized user {ctx.author}')
        log_lines = ''
        with open(utils.DBOT_LOG_FILE, 'r') as log:
            log_lines = ''.join(log.readlines()[-n:])
        await ctx.reply(f'```{log_lines}```')

    @commands.command(help='Check DBot Latency')
    async def ping(self, ctx):
        async with ctx.typing():
            em = discord.Embed(color=discord.Color.green())
            em.title = "Ping Response"
            em.description = f'{self.bot.latency * 1000:0.2f} ms'
        await ctx.send(embed=em)

    @commands.command(aliases=['sd'], hidden=True)
    @utils.dev_only()
    async def shutdown(self, ctx) -> None:
        logger.warning(f'SHUTDOWN REQUESTED FROM VALID DEVELOPER {ctx.author}')
        logger.warning(f'Providing most recent log before shutdown.')
        await ctx.send(f"DBot is shutting down at {ctx.author}'s request.")
        await ctx.send(f'Providing most recent log before shutdown.')
        await ctx.send(file=discord.File(str(utils.DBOT_LOG_FILE)))
        await self.bot.change_presence(activity=None, status=discord.Status.offline, afk=True)
        await self.bot.close()

    @commands.command(name='uptime', help='DBot Uptime')
    async def uptime(self, ctx) -> None:
        up = self.start_time - datetime.datetime.now()
        async with ctx.typing():
            '''Current bot instance uptime'''
            em = discord.Embed(color=discord.Color.green())
            em.title = 'DBot Uptime'
            em.description = str(datetime.datetime.now() - self.start_time)
            em.set_footer(text="DBot is powered by discord.py")
        await ctx.send(embed=em)


def setup(bot: commands.Bot) -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    bot.add_cog(BotAdmin(bot))