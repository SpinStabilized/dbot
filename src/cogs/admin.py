# -*- coding: utf-8 -*-
import discord
import logging

from discord.ext import commands

import utils.sec

logger = logging.getLogger('dbot')

class BotAdmin(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot
        logger.info('BotAdmin Cog Loaded')
    
    @commands.command(aliases=['sd'], hidden=True)
    @utils.sec.dev_only()
    async def shutdown(self, ctx, *, foo=None) -> None:
        logger.warning(f'SHUTDOWN REQUESTED FROM VALID DEVELOPER {ctx.author}')
        await ctx.send(f"DBot is shutting down at {ctx.author}'s request.")
        await self.bot.change_presence(activity=None, status=discord.Status.offline, afk=True)
        await self.bot.logout()

    @commands.command(name='about')
    async def about(self, ctx) -> None:
        async with ctx.typing():
            '''Shows info about bot'''
            em = discord.Embed(color=discord.Color.green())
            em.title = 'About DBot'
            em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            em.description = 'The DBot'
            em.add_field(name="Servers", value=len(self.bot.guilds))
            em.add_field(name="Bot Latency", value=f"{self.bot.ws.latency * 1000:.0f} ms")
            em.add_field(name="Invite Me To Your Server", 
                         value=f"[Click Here](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=268905542)")

            em.set_footer(text="DBot is powered by discord.py")
        await ctx.send(embed=em)

    @commands.command()
    async def ping(self, ctx):
        async with ctx.typing():
            em = discord.Embed(color=discord.Color.green())
            em.title = "Ping Response"
            em.description = f'{self.bot.latency * 1000:0.2f} ms'
        await ctx.send(embed=em)

def setup(bot: "Bot") -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    bot.add_cog(BotAdmin(bot))