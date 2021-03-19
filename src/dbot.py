# -*- coding: utf-8 -*-
import discord
import logging
import logging.handlers
import os
import platform
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
PREFIX = os.getenv('DISCORD_BOT_PREFIX')
bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(f"with {len(bot.guilds)} servers"), afk=True)
    logger.info(f'Logged in as {bot.user.name}')
    logger.info(f'Discord.py API version: {discord.__version__}')
    logger.info(f'Python version: {platform.python_version()}')
    logger.info(f'Running on: {platform.system()} {platform.release()} ({os.name})')

@bot.event
async def on_guild_join(g):
    await bot.change_presence(activity=discord.Game(f"with {len(bot.guilds)} servers"), afk=True)

@bot.event
async def on_guild_remove(g):
    await bot.change_presence(activity=discord.Game(f"with {len(bot.guilds)} servers"), afk=True)

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandNotFound):  # fails silently
        await ctx.reply(error)

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f'This command is on cooldown. Please wait {error.retry_after:.2f}s')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply('You do not have the permissions to use this command.')
    # If any other error occurs, prints to console.
    else:
        logger.error(''.join(traceback.format_exception(type(error), error, error.__traceback__)))

if __name__ == "__main__":

    cog_extensions = [
        'cogs.rolldice',
        'cogs.admin',
        'cogs.bgg'
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
