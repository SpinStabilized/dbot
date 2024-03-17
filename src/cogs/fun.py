# -*- coding: utf-8 -*-
"""Some functions just for fun for the DBot discord bot.

"""
import logging
import os
import subprocess

import discord
from discord.ext import commands

import utils

logger: logging.Logger = utils.get_dbot_logger()

PREFIX: str = os.getenv('DISCORD_BOT_PREFIX')

# Determine the system path to the commands used in this Cog
COWSAY: str = subprocess.run(['which', 'cowsay'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        text=True
                        ).stdout.strip()
COWTHINK:str  = subprocess.run(['which', 'cowthink'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.STDOUT, 
                         text=True).stdout.strip()
FORTUNE:str = subprocess.run(['which', 'fortune'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.STDOUT,
                         text=True).stdout.strip()

################################################################################
# Help Documentation
################################################################################

#######################################
# cowsay command help
#######################################
FUN_COWSAY_HELP_BRIEF: str = 'The cow says "Moo" or whatever you want.'
FUN_COWSAY_HELP_LONG: str = f"""
{FUN_COWSAY_HELP_BRIEF}

Example:
\t>{PREFIX}cowsay "DBot Rocks!"

\t _______________ 
\t< "DBot Rocks!" >
\t --------------- 
\t        \\   ^__^
\t         \\  (oo)\\_______
\t            (__)\\       )\\/\\
\t                ||----w |
\t                ||     ||
"""

#######################################
# cowthink command help
#######################################
FUN_COWTHINK_HELP_BRIEF: str = 'The cow thinks "Moo" or whatever you want.'
FUN_COWTHINK_HELP_LONG: str = f"""
{FUN_COWTHINK_HELP_BRIEF}

Example:
\t>{PREFIX}cowthink "DBot Rocks!"

\t _______________ 
\t( "DBot Rocks!" )
\t --------------- 
\t        o   ^__^
\t         o  (oo)\\_______
\t            (__)\\       )\\/\\
\t                ||----w |
\t                ||     ||
"""

#######################################
# fortune command help
#######################################
FUN_FORTUNE_HELP_BRIEF: str = 'Display a fortune from the famous UNIX command.'
FUN_FORTUNE_HELP_LONG: str = f"""
{FUN_FORTUNE_HELP_BRIEF}

Example:
\t>{PREFIX}fortune
\t"Hello again, Peabody here..."
\t-- Mister Peabody
"""


class FunBot(commands.Cog, name='Some additional "fun"ctionality.'):
    """Some fun commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        logger.info('FunBot Cog Loaded')
    
    ############################################################################
    # fortune command
    ############################################################################
    @commands.command(
            brief=FUN_FORTUNE_HELP_BRIEF,
            help=FUN_FORTUNE_HELP_LONG,
    )
    async def fortune(self, ctx: commands.Context):
        """Displays a fortune cookie message.

        This command generates a random fortune message using the 'fortune'
        command-line tool. The generated message is then sent as an embedded
        message to the Discord channel where the command was invoked.

        Parameters:
            ctx (commands.Context): The context object representing the
                                    invocation context.

        Returns:
            None

        Raises:
            None
        """
        async with ctx.typing():
            data:str = subprocess.run([FORTUNE], 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    text=True).stdout.strip()
            em: discord.Embed = discord.Embed(color=discord.Color.light_grey())
            em.title = f'Fortune'
            em.description = data
        await ctx.send(embed=em)

    ############################################################################
    # cowsay command
    ############################################################################
    @commands.command(
            aliases=['cs'],
            brief=FUN_COWSAY_HELP_BRIEF,
            help=FUN_COWSAY_HELP_LONG,
    )
    async def cowsay(self, ctx: commands.Context, *, 
        message: str = commands.parameter(default='Moo', description='Message for the cow to say.')):
        """Generates a cow ASCII art with a custom message using the 'cowsay' command-line tool.

        This command generates a cow ASCII art with a custom message provided by
        the user. If no message is provided, the default message "Moo" is used.
        The generated ASCII art is then sent as a code block in the Discord
        channel where the command was invoked.

        Parameters:
            ctx (commands.Context): The context object representing the
                                    invocation context.
            message (str, optional): The message for the cow to say. Defaults
                                     to "Moo".

        Returns:
            None

        Raises:
            None
        """
        logger.info(f'\t{message}')
        async with ctx.typing():
            args: list[str] = message.split(' ')
            data: str = subprocess.run([COWSAY] + args, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True).stdout
        await ctx.send(f'```{data}```')

    ############################################################################
    # cowthink command
    ############################################################################
    @commands.command(
            aliases=['ct'],
            brief=FUN_COWTHINK_HELP_BRIEF,
            help=FUN_COWTHINK_HELP_LONG,
    )
    async def cowthink(self, ctx: commands.Context, *,
        message:str = commands.parameter(default='Moo', description='Message for the cow to think.')):
        """Generates a cow ASCII art with a custom message using the 'cowthink' command-line tool.

        This command generates a cow ASCII art with a custom message provided by
        the user. If no message is provided, the default message "Moo" is used.
        The generated ASCII art is then sent as a code block in the Discord
        channel where the command was invoked.

        Parameters:
            ctx (commands.Context): The context object representing the
                                    invocation context.
            message (str, optional): The message for the cow to think. Defaults
                                     to "Moo".

        Returns:
            None

        Raises:
            None
        """
        logger.info(f'\t{message}')
        async with ctx.typing():
            args: list[str] = message.split(' ')
            data: str = subprocess.run([COWTHINK] + args,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT,
                   text=True).stdout
        await ctx.send(f'```{data}```')


async def setup(bot: commands.Bot) -> None:
    """Add this Cog to the identified Bot.

    Parameters
    ----------
    bot (commands.Bot): The Bot that this Cog will be added to.
    
    """
    await bot.add_cog(FunBot(bot))