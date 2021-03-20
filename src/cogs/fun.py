# -*- coding: utf-8 -*-
import cowsay
import discord
import logging

from discord.ext import commands

logger = logging.getLogger('dbot')

class FunBot(commands.Cog):

    def __init__(self, bot:'Bot') -> None:
        self.bot = bot
        logger.info('FunBot Cog Loaded')
    
    @commands.command(aliases=['cs'], help='Fun message from a cow')
    async def cowsay(self, ctx, *, message='Moo'):
        msg_words = message.split(' ')
        creature = msg_words[0] \
            if msg_words[0] in cowsay.char_names \
                else 'cow'
        send_msg = ' '.join(msg_words[1:]) \
            if creature != 'cow' \
                else message
        fn = cowsay.chars[list(cowsay.char_names).index(creature)] \
            if creature in cowsay.char_names \
                else cowsay.chars[list(cowsay.char_names).index('cow')]
        await ctx.send(f'```{fn(send_msg)}```')


def setup(bot: "Bot") -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    bot.add_cog(FunBot(bot))