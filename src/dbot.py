# -*- coding: utf-8 -*-
"""The DBot, yet another custom discord bot.


"""
import discord
import dotenv
import logging
import os
import platform
import traceback

from discord.ext import commands

import utils

logger: logging.Logger = utils.dbot_logger_config()

dotenv.load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')
PREFIX: str = os.getenv('DISCORD_BOT_PREFIX')

bot_intents: discord.Intents = discord.Intents.default()
bot_intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix=PREFIX, intents=bot_intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(f"with {len(bot.guilds)} servers"))
    logger.info(f'Logged in as {bot.user.name}')
    logger.info(f'Discord.py API version: {discord.__version__}')
    logger.info(f'Python version: {platform.python_version()}')
    logger.info(f'Running on: {platform.system()} {platform.release()} ({os.name})')

    cog_extensions: list[str] = [
        'cogs.rolldice',
        'cogs.admin',
        'cogs.bgg',
        'cogs.fun'
    ]

    for cog_ext in cog_extensions:
        try:
            logger.info(f'Loading {cog_ext}')
            await bot.load_extension(cog_ext)
        except Exception as e:
            logger.error(e)

@bot.before_invoke
async def log_command(ctx: commands.Context):
    logger.info(f'User {ctx.author} on server {ctx.guild} in channel {ctx.channel} invoked command {ctx.command.name} from cog {ctx.command.cog_name}')

@bot.event
async def on_guild_join(g: discord.Guild):
    logger.info(f'DBot Added To Server {g.name} owned by {g.owner}')
    await bot.change_presence(activity=discord.Game(f'with {len(bot.guilds)} servers'))

@bot.event
async def on_guild_remove(g: discord.Guild):
    logger.info(f'DBot Removed From Server {g.name} owned by {g.owner}')
    await bot.change_presence(activity=discord.Game(f'with {len(bot.guilds)} servers'))

@bot.event
async def on_command_error(ctx: commands.Context, error: discord.DiscordException):

    if isinstance(error, commands.CommandNotFound): 
        await ctx.reply(error)

    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f'This command is on cooldown. Please wait {error.retry_after:.0f}s')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply('You are not authorized to use this command.')

    else:
        logger.error(''.join(traceback.format_exception(type(error), error, error.__traceback__)))

if __name__ == "__main__":

    try:
        logger.info(f'Starting Bot...')
        bot.run(TOKEN)
    except Exception as e:
        print(f'Error when logging in: {e}')
        logger.error(f'Error when logging in: {e}')
