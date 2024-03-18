# -*- coding: utf-8 -*-
"""Contains administrative functions for managing DBot.

This module provides administrative commands for managing various aspects of DBot, 
such as providing information about the bot, calculating mathematical expressions, 
retrieving log information, checking bot latency, shutting down the bot, and displaying 
the bot's uptime.

Attributes:
    PREFIX (str): The command prefix for DBot.
    logger (logging.Logger): The logger instance for DBot.

Commands:
    - about: Provides information about the bot.
    - calc: Calculates the result of a mathematical expression.
    - log_get: Retrieves the log file and sends it to the invoking user (restricted to authorized developers).
    - log_tail: Retrieves the last 'n' lines from the log file and sends them to the invoking user (restricted to authorized developers).
    - ping: Calculates and sends the bot's latency in milliseconds as an embedded message.
    - shutdown: Shuts down the bot gracefully upon a developer's request (restricted to authorized developers).
    - uptime: Displays the uptime of the bot since it was last started.

Example:
    To access the about command:
    ```
    <prefix>about
    ```

    To calculate a mathematical expression:
    ```
    <prefix>calc 2 + 2
    ```

    To retrieve the log file:
    ```
    <prefix>log_get
    ```

    To retrieve the last 10 lines from the log file:
    ```
    <prefix>log_tail 10
    ```

    To check the bot's latency:
    ```
    <prefix>ping
    ```

    To shut down the bot:
    ```
    <prefix>shutdown
    ```

    To check the bot's uptime:
    ```
    <prefix>uptime
    ```
"""

import datetime
import logging
import os
import platform

import discord
from discord.ext import commands

import utils

logger: logging.Logger = utils.get_dbot_logger()

PREFIX: str = os.getenv('DISCORD_BOT_PREFIX')


################################################################################
# Help Documentation
################################################################################

#######################################
# about command help
#######################################
ADMIN_ABOUT_HELP_BRIEF = 'About DBot'
ADMIN_ABOUT_HELP_LONG = f"""
{ADMIN_ABOUT_HELP_BRIEF}

Example:
\t>{PREFIX}about

"""

#######################################
# calc command help
#######################################
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

#######################################
# ping command help
#######################################
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
    """Contains administrative functions for managing DBot.

    This class provides a collection of commands for managing various administrative
    functions of DBot, such as providing information about the bot, calculating
    mathematical expressions, retrieving log information, checking bot latency,
    shutting down the bot, and displaying the bot's uptime.

    Attributes:
        bot (commands.Bot): The bot instance associated with the cog.
        start_time (datetime.datetime): The datetime when the bot cog was initiated.

    Example:
        To access the about command:
        ```
        <prefix>about
        ```

        To calculate a mathematical expression:
        ```
        <prefix>calc 2 + 2
        ```

        To retrieve the log file:
        ```
        <prefix>log_get
        ```

        To retrieve the last 10 lines from the log file:
        ```
        <prefix>log_tail 10
        ```

        To check the bot's latency:
        ```
        <prefix>ping
        ```

        To shut down the bot:
        ```
        <prefix>shutdown
        ```

        To check the bot's uptime:
        ```
        <prefix>uptime
        ```
    """
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        logger.info('BotAdmin Cog Loaded')
        self.start_time: datetime.datetime = datetime.datetime.now()

    ############################################################################
    # about command
    ############################################################################
    @commands.command(
            brief=ADMIN_ABOUT_HELP_BRIEF,
            help=ADMIN_ABOUT_HELP_LONG,
    )
    async def about(self, ctx: commands.Context) -> None:
        """Provides information about the bot.

        This method generates an embed containing various details about the bot,
        such as its name, the number of servers it is in, its latency, uptime,
        source repository link, invite link, discord.py version, Python version,
        and environment details.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        async with ctx.typing():
            em: discord.Embed = discord.Embed(color=discord.Color.green())
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

    ############################################################################
    # calc command
    ############################################################################
    @commands.command(
            brief=ADMIN_CALC_HELP_BRIEF,
            help=ADMIN_CALC_HELP_LONG,
    )
    async def calc(self, ctx: commands.Context, 
            calculation: str = commands.parameter(default='0', description='Math expression')):
        """Calculates the result of a mathematical expression.

        This method evaluates the provided mathematical expression and returns
        the result. If the expression is invalid or contains syntax errors, it
        returns an error message.

        Parameters:
            ctx (commands.Context): The context of the command.
            calculation (str, optional): The mathematical expression to be
                                         evaluated. Defaults to '0'.

        Returns:
            None
        """
        logger.info(f'\t{calculation}')
        async with ctx.typing():
            result_str: str = ''
            try:
                result: float = utils.eval_expr(calculation)
                result_str = f'Results: {result}'
            except SyntaxError as se:
                result_str = '```Syntax Error In Expression\n'
                result_str += f'\t{se.text}\n'
                result_str += f'\t{" " * (se.offset-1)}^```'
        await ctx.reply(result_str)

    ############################################################################
    # log_get command
    ############################################################################
    @commands.command(hidden=True)
    @utils.dev_only()
    async def log_get(self, ctx: commands.Context):
        """Retrieves the log file and sends it to the invoking user.

        This method is restricted to authorized developers only. It retrieves
        the log file containing the bot's activity and sends it as an attachment
        to the user who invoked the command.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        await ctx.reply(file=discord.File(str(utils.DBOT_LOG_FILE)))

    ############################################################################
    # log_tail command
    ############################################################################
    @commands.command(hidden=True)
    @utils.dev_only()
    async def log_tail(self, ctx: commands.Context, n: int = 10):
        """Retrieves the last 'n' lines from the log file and sends them to the invoking user.

        This method is restricted to authorized developers only. It retrieves
        the last 'n' lines from the log file containing the bot's activity and
        sends them as a code block to the user who invoked the command.

        Parameters:
            ctx (commands.Context): The context of the command.
            n (int, optional): The number of lines to retrieve from the end of
                               the log file. Defaults to 10.

        Returns:
            None
        """
        logger.info(f'\t{n} lines of the logfile requested')
        log_lines: str = ''
        with open(utils.DBOT_LOG_FILE, 'r') as log:
            log_lines = ''.join(log.readlines()[-n:])
        await ctx.reply(f'```{log_lines}```')

    ############################################################################
    # ping command
    ############################################################################
    @commands.command(
            brief=ADMIN_PING_HELP_BRIEF,
            help=ADMIN_PING_HELP_LONG,
    )
    async def ping(self, ctx: commands.Context):
        """Calculates and sends the bot's latency in milliseconds as an embedded message.

        This command retrieves the bot's latency, which is the time taken for a
        message to be sent from the Discord gateway to the bot and back,
        measured in milliseconds. The latency value is then embedded in a
        message and sent to the channel where the command was invoked.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        async with ctx.typing():
            em: discord.Embed = discord.Embed(color=discord.Color.green())
            em.title = "Ping Response"
            em.description = f'{self.bot.latency * 1000:0.2f} ms'
        await ctx.send(embed=em)

    ############################################################################
    # shutdown command
    ############################################################################
    @commands.command(aliases=['sd'], hidden=True)
    @utils.dev_only()
    async def shutdown(self, ctx: commands.Context) -> None:
        """Shuts down the bot gracefully upon a developer's request.

        This command allows authorized developers to shut down the bot
        gracefully. It sends a message to the current Discord channel indicating
        that the bot is shutting down, and provides the most recent log file
        before the shutdown. After sending the log file, it changes the bot's
        presence to offline and closes the bot's connection to Discord.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        logger.warning(f'Providing most recent log before shutdown.')
        await ctx.send(f"DBot is shutting down at {ctx.author}'s request.")
        await ctx.send(f'Providing most recent log before shutdown.')
        await ctx.send(file=discord.File(str(utils.DBOT_LOG_FILE)))
        await self.bot.change_presence(activity=None, status=discord.Status.offline)
        
        await self.bot.close()

    ############################################################################
    # uptime command
    ############################################################################
    @commands.command(
            brief=ADMIN_UPTIME_HELP_BRIEF,
            help=ADMIN_UPTIME_HELP_LONG,
    )
    async def uptime(self, ctx: commands.Context) -> None:
        """Displays the uptime of the bot since it was last started.

        This command provides information about the duration for which the bot
        has been running since it was last started. It calculates the difference
        between the current date and time and the time when the bot was started,
        and then sends this information as a message with an embedded format.

        Parameters:
            ctx (commands.Context): The context of the command.

        Returns:
            None
        """
        async with ctx.typing():
            em: discord.Embed = discord.Embed(color=discord.Color.green())
            em.title = 'DBot Uptime'
            em.description = str(datetime.datetime.now() - self.start_time)
            em.set_footer(text="DBot is powered by discord.py")
        await ctx.send(embed=em)


async def setup(bot: commands.Bot) -> None:
    """Add this Cog to the identified Bot.

    Parameters
    ----------
    bot (commands.Bot): 
        The Bot that this Cog will be added to.
    
    """
    await bot.add_cog(BotAdmin(bot))