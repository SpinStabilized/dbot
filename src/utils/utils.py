import logging
import os

from discord.ext import commands
from typing import Final

DBOT_LOGGER_ID: Final[str] = 'dbot'
logger = logging.getLogger(DBOT_LOGGER_ID)

def dbot_logger_config() -> logging.Logger:
    logger: logging.Logger = logging.getLogger('dbot')
    logger.setLevel(logging.DEBUG)
    # handler = logging.handlers.RotatingFileHandler(filename='dbot.log', encoding='utf-8',maxBytes=1024*1024, backupCount=10)
    handler: logging.handlers.StreamHandler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    )
    logger.addHandler(handler)
    return logger

def get_dbot_logger() -> logging.Logger:
    return logging.getLogger(DBOT_LOGGER_ID)

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



