import logging
import os

from discord.ext import commands

logger = logging.getLogger('dbot')

def dev_only():
    async def wrapper(ctx):
        devs_raw = os.getenv('DISCORD_BOT_DEVELOPERS')
        devs = [int(d) for d in devs_raw.split(';')]
        if ctx.author.id in devs:
            return True
        logger.warn(f'Unauthorized Command Use Attempted By {ctx.author}.')
        # 
        await ctx.reply('You are not authorized to use this command.')
        raise commands.MissingPermissions(['developer'])
        return False
    return commands.check(wrapper)