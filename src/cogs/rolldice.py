# -*- coding: utf-8 -*-
"""Some functions just for fun for the DBot discord bot.

"""
import argparse
import datetime
import logging
import os
import pathlib
import random
import re
import statistics

import discord
from discord.ext import commands

import utils

###############################################################################
# Configure the MPLCONFIGDIR environmental variable to give matplotlib a place
# to work in the user access area in the Docker container.
###############################################################################
mpl_config = pathlib.Path.cwd() / 'mpl_config'
mpl_config.mkdir(parents=True, exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(mpl_config)
###############################################################################

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

mpl.use('Agg')
logger: logging.Logger = utils.get_dbot_logger()

PREFIX: str = os.getenv('DISCORD_BOT_PREFIX')

################################################################################
# Help Documentation
################################################################################

#######################################
# roll command help
#######################################
ROLL_HELP_BRIEF: str = 'Roll a virtual set of dice.'
ROLL_HELP_LONG: str = f"""
{ROLL_HELP_BRIEF}

Example:
\t>{PREFIX}roll 1d20
\t[**20**] = 20

"""

#######################################
# roll_sim command help
#######################################
ROLL_SIM_HELP_BRIEF: str = 'Dice roll simulator/statistics generator'
ROLL_SIM_HELP_LONG: str = f"""
{ROLL_SIM_HELP_BRIEF}

Example:
\t>{PREFIX}roll_sim 1d20
\tDisplay a plot of the dice statistics.

"""

class RollDice(commands.Cog, name='Dice Rolling'):
    """Dice rolling cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info('RollDice Cog Loaded')

    ############################################################################
    # roll command
    ############################################################################
    @commands.command(
            aliases=['r'],
            brief=ROLL_HELP_BRIEF,
            help=ROLL_HELP_LONG,
    )
    async def roll(self, ctx: commands.Context, *, 
        dice_string: str = commands.parameter(default='1d20', description='Dice roll expression')) -> None:
        """
        Rolls dice based on the provided expression and sends the result to the Discord channel.

        This command rolls dice based on the provided dice roll expression.
        If no expression is provided, it defaults to rolling a single 20-sided
        die (1d20). The results of the dice roll, along with the total, are sent
        as a reply to the Discord channel where the command was invoked.

        Parameters:
            ctx (commands.Context): The context object representing the
                                             invocation context.
            dice_string (str, optional): The dice roll expression. Defaults
                                         to "1d20".

        Returns:
            None

        Raises:
            None
        """
        logger.info(f'\t{dice_string}')
        
        roll_exception: Exception | None = None
        async with ctx.typing():
            try:
                results: str = ''
                total: int = 0
                results, total = Die.dice_roller(dice_string)
            except SyntaxError as se:
                roll_exception: SyntaxError = se
                logger.exception(se)
        if roll_exception:
            await ctx.reply(f'Error In Dice Roll')
        else:
            await ctx.reply(f'{results} = {total}')
            logger.info(f'\tResult: {results} = {total}')

    ############################################################################
    # roll_sim command
    ############################################################################
    @commands.command(
            brief=ROLL_SIM_HELP_BRIEF,
            help=ROLL_SIM_HELP_LONG,
    )
    async def roll_sim(self, ctx: commands.Context, *, 
        dice_string: str = commands.parameter(default='1d20', description='Dice roll expression')) -> None:
        """Simulates multiple dice rolls based on the provided expression and sends a plot of the resulting statistics as an image to the Discord channel.

        This command simulates multiple dice rolls based on the provided dice
        roll expression. If no expression is provided, it defaults to simulating
        a single 20-sided die (1d20). The simulation is run a default of 10,000
        times, or the specified number of times if provided.
        
        The results of the simulation are displayed as a histogram image in the
        Discord channel where the command was invoked.

        Parameters:
            ctx (commands.Context): The context object representing the invocation context.
            dice_string (str, optional): The dice roll expression. Defaults to "1d20".

        Returns:
            None

        Raises:
            None
        """
        roll_exception: Exception = None
        async with ctx.typing():
            parser: argparse.ArgumentParser = argparse.ArgumentParser()
            parser.add_argument('-n', '--n_times', default=10000, type=int)
            parser.add_argument('roll_spec', nargs='*')
            args: argparse.Namespace = parser.parse_args(dice_string.split())
            args.roll_spec = ' '.join(args.roll_spec)

            logger.info(f'\t{dice_string}')
            if args.n_times > 10000:
                args.n_times = 10000
            try:
                fname: tuple[float, float, str] = Die.dice_sim(args.roll_spec, args.n_times)
            except SyntaxError as se:
                roll_exception: SyntaxError = se
                logger.exception(se)
            
        if roll_exception:
            await ctx.reply(f'Error In Dice Roll')
        else:
            p_file: discord.File = discord.File(fname, filename='image.png')
            embed: discord.Embed = discord.Embed(
                title='Dice Roll Simulator',
                color=0x00ff00
            )
            embed.set_image(url='attachment://image.png')
            await ctx.reply(embed=embed, file=p_file)
            os.remove(fname)


class Die:
    """An object that models a die roll and tracks critical hits/fails.

    Parameters
    ----------
    sides (int): Number of sides for the die.
    exploded (bool): Identifies if this dice roll was from an exploded roll.
    
    """

    def __init__(self, sides: int, exploded: bool=False) -> None:
        self.sides: int = sides
        self.exploded: bool = exploded
        self.keep: bool = True
        self.roll

    DICE_REGEX: re.Pattern = re.compile(r'(\d+d\d+[!]{0,1}(?:[k|d]\d+){0,1})')
    """re.Pattern : A regex string find dice rolls in a larger string."""

    DICE_SPEC: re.Pattern = re.compile(r'(\d+)d(\d+)([!]{0,1})((?:[k|d]\d+){0,1})')
    """re.Pattern : A regex string to define the components of a die roll."""

    @classmethod
    def multi_roll(cls, dice_spec: str) -> list:
        """Roll a number of dice with a specified number of sides.

        Parameters
        ----------
        dice_spec (str): The specfication of the dice to roll in ``xdy`` format
                         where ``x`` is the number of dice to roll and ``y`` is
                         the number of sides each die will have.
        
        Returns
        -------
        list[Die]: A list of the roll results.

        """
        parsed: list[tuple[str, str, str, str]] = re.findall(Die.DICE_SPEC, dice_spec)
        dice_string: str = ''
        sides_string: str = ''
        explode_string: str = ''
        keep_drop: str = ''
        dice_string, sides_string, explode_string, keep_drop = \
            parsed[0] if parsed else (None, None, None, None)
        
        dice: int = int(dice_string)
        sides: int = int(sides_string)
        explode: bool =  bool(explode_string)
        
        results: list[Die] = [cls(sides) for _ in range(dice)]
        results.sort(key=lambda x: x.value)
        if explode == '!':
            explode_results: list[Die] = []
            for r in results:
                explode_results.append(r)
                while explode_results[-1].critical_hit:
                    explode_results.append(cls(sides, True))
            results = explode_results[:]

        if keep_drop:
            fn: str = keep_drop[0]
            number: int = int(keep_drop[1:])
            results.sort(key=lambda x: x.value)
            if fn == 'k':
                keep: list[Die] = results[-number:]
                drop: list[Die] = results[:-number]
                for d in drop: d.keep = False
                results = drop + keep
            elif fn == 'd':
                keep: list[Die] = results[:-number]
                drop: list[Die] = results[-number:]
                for d in drop: d.keep = False
                results = keep + drop
        return results

    @staticmethod
    def dice_roller(roll: str) -> tuple[str, int]:
        """Processes a dice roll string.

        Parameters
        ----------
        roll (str): A dice roll string specification.
        
        Returns
        -------
        tuple[str, int]: A string that shows the results of the dice rolls and
                         the total value of the rolls.
        
        """
        roll_exp: str = roll
        dice_rolls: list[str] = re.findall(Die.DICE_REGEX, roll)
        dice_results: list[Die] = [Die.multi_roll(r) for r in dice_rolls]
        for i, r in enumerate(dice_rolls):
            str_result: str = '+'.join([str(d.value) for d in dice_results[i]])
            fstr_result: str = '+'.join([str(d) for d in dice_results[i]])
            str_result_disp: str = f'[{fstr_result}]'
            str_result_exp: str = f'({str_result})'
            roll: str = roll.replace(r, str_result_disp, 1)
            roll_exp: str = roll_exp.replace(r, str_result_exp, 1)
        
        result: int = int(utils.eval_expr(roll_exp))
        return roll, result

    @staticmethod
    def dice_sim(roll: str, n: int = 10000) -> tuple[float, float, str]:
        """Simulate dice rolls repeatedly to collect statistics.

        Parameters
        ----------
        roll (str): The dice roll specification.
        n (int): Number of iterations to execute.

        """
        results: list[int] = [Die.dice_roller(roll)[1] for _ in range(n)]
        r_min: int = min(results)
        r_max: int = max(results)
        mean: float = statistics.fmean(results)
        stdev: float = statistics.stdev(results)
        num_bins: int = (r_max - r_min) + 1
        fig, ax = plt.subplots()
        h_data, bins, patches = ax.hist(results, num_bins, density=True)

        ax.set_xlabel('Result')
        ax.set_ylabel('Probability Density')
        ax.set_title(f'Histogram of {roll} Rolled {n:,} Times\n$\\mu={mean:0.0f}, \\sigma={stdev:0.2f}$')
        now: datetime.datetime = datetime.datetime.now()
        fname = f'/tmp/dbot_roll_sim_{now.strftime("%Y_%m_%d_%H_%M_%S")}.png'
        fig.tight_layout()
        fig.savefig(fname)
        logger.debug(fname)

        return fname

    def __str__(self):
        ret_val = str(self.__value)
        if self.critical_hit or self.critical_fail:
            ret_val = f'**{ret_val}**'
        if self.exploded:
            ret_val = f'__{ret_val}__'
        if not self.keep:
            ret_val = f'~~{ret_val}~~'
        return ret_val

    @property
    def roll(self) -> int:
        """Roll the die.

        This doesn't have to be called expicitly unless there is a desire to
        roll multiple times. It is called as part of object initilization.

        Returns
        -------
        (int): The value of the roll.
        """
        self.__value =  random.choice(range(1, self.sides + 1))
        return self.__value
    
    @property
    def value(self) -> int:
        """The value of the last roll.

        Returns
        -------
        (int): The value of the last die roll.

        """
        return self.__value if self.keep else 0
    
    @property
    def critical_hit(self) -> bool:
        """Identifies if the last roll was a critical hit.

        Returns
        -------
        (bool): True if the last roll was a critical hit.

        """
        return self.__value == self.sides
    
    @property
    def critical_fail(self) -> bool:
        """Identifies if the last roll was a critical fail.

        Returns
        -------
        (bool): True if the last roll was a critical fail.
        
        """
        return self.__value == 1

async def setup(bot: commands.Bot) -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot (command.Bot): The Bot that this Cog will be added to.
    
    """
    await bot.add_cog(RollDice(bot))