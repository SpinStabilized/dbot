# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import signal
import sys

from discord.ext import commands
from dotenv import load_dotenv

logger = logging.getLogger('dbot')
logger.setLevel(logging.DEBUG)
# handler = logging.handlers.RotatingFileHandler(filename='dbot.log', encoding='utf-8',maxBytes=1024*1024, backupCount=10)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
)
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
PREFIX = os.getenv('DISCORD_BOT_PREFIX')
bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} has connected to Discord!')

if __name__ == "__main__":

    cog_extensions = [
        'cogs.rolldice'
    ]

    for cog_ext in cog_extensions:
        try:
            logger.info(f'Loading {cog_ext}')
            bot.load_extension(cog_ext)
        except Exception as e:
            logger.error(e)

    try:
        logger.info(f'Starting Bot...')
        bot.run(TOKEN)
    except Exception as e:
        print(f'Error when logging in: {e}')
        logger.error(f'Error when logging in: {e}')
