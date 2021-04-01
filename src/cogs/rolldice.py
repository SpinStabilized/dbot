# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
import logging
import math
import os
import pathlib
import random
import re
import statistics

###############################################################################
# Configure the MPLCONFIGDIR environmental variable to give matplotlib a place
# to work in the user access area in the Docker container.
###############################################################################
mpl_config = pathlib.Path.cwd() / 'mpl_config'
mpl_config.mkdir(parents=True, exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(mpl_config)
###############################################################################

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import discord
from discord.ext import commands
from typing import List, Tuple

import utils

logger = utils.get_dbot_logger()

class RollDice(commands.Cog):
    """Dice rolling cog."""

    def __init__(self, bot: "Bot"):
        self.bot = bot
        logger.info('RollDice Cog Loaded')
    
    @commands.command(aliases=['r'], help='Simulates rolling dice.')
    async def roll(self, ctx, *, dice_string: str = None) -> None:
        logger.info(f'Roll request from {ctx.author}')
        logger.info(f'\t{dice_string}')
        
        roll_exception = None
        async with ctx.typing():
            try:
                results, total = Die.dice_roller(dice_string)
            except SyntaxError as se:
                roll_exception = se
                logger.exception(se)
        if roll_exception:
            await ctx.reply(f'Error In Dice Roll')
        else:
            await ctx.reply(f'{results} = {total}')
            logger.info(f'\tResult: {results} = {total}')

    @commands.command(help='Dice roll simulator/statistics generator')
    async def roll_sim(self, ctx, *, dice_string: str = None) -> None:
        roll_exception = None
        async with ctx.typing():
            parser = argparse.ArgumentParser()
            parser.add_argument('-n', '--n_times', default=10000, type=int)
            parser.add_argument('roll_spec', nargs='*')
            args = parser.parse_args(dice_string.split())
            args.roll_spec = ' '.join(args.roll_spec)

            logger.info(f'Simulating dice roll from {ctx.author}')
            logger.info(f'\t{dice_string}')
            try:
                mean, stdev, fname = Die.dice_sim(args.roll_spec, args.n_times)
            except SyntaxError as se:
                roll_exception = se
                logger.exception(se)
            
        if roll_exception:
            await ctx.reply(f'Error In Dice Roll')
        else:
            p_file = discord.File(fname, filename='image.png')
            embed = discord.Embed(
                title='Dice Roll Simulator',
                description=f'Statistical results of rolling {args.roll_spec} {args.n_times:,} times.',
                color=0x00ff00
            )
            embed.set_image(url='attachment://image.png')
            embed.add_field(name='Mean', value=f'{mean:0.2f}', inline=True)
            embed.add_field(name='Standard Deviation', value=f'{stdev:0.2f}', inline=True)
            await ctx.reply(embed=embed, file=p_file)


class Die:
    """An object that models a die roll and tracks critical hits/fails.

    Parameters
    ----------
    sides : :obj:`int`
        Number of sides for the die.
    exploded : :obj:`bool`
        Identifies if this dice roll was from an exploded roll.
    
    """

    def __init__(self, sides:int, exploded:bool=False) -> None:
        self.sides = sides
        self.exploded = exploded
        self.keep = True
        self.roll

    DICE_REGEX = re.compile(r'(\d+d\d+[!]{0,1}(?:[k|d]\d+){0,1})')
    """:obj:`str` : A regex string find dice rolls in a larger string."""

    DICE_SPEC = re.compile(r'(\d+)d(\d+)([!]{0,1})((?:[k|d]\d+){0,1})')
    """:obj:`str` : A regex string to define the components of a die roll."""

    @classmethod
    def multi_roll(cls, dice_spec: str) -> List:
        """Roll a number of dice with a specified number of sides.

        Parameters
        ----------
        dice_spec : :obj:`str`
            The specfication of the dice to roll in ``xdy`` format where ``x`` is
            the number of dice to roll and ``y`` is the number of sides each die
            will have.
        
        Returns
        -------
        :obj:`list` of :obj:`Die`
            A list of the roll results.

        """
        parsed = re.findall(Die.DICE_SPEC, dice_spec)
        dice, sides, explode, keep_drop = \
            parsed[0] if parsed else (None, None, None, None)
        dice, sides, exploded = \
            int(dice), int(sides), bool(explode)
        
        results = [cls(sides) for _ in range(dice)]
        results.sort(key=lambda x: x.value)
        if explode == '!':
            explode_results = []
            for r in results:
                explode_results.append(r)
                while explode_results[-1].critical_hit:
                    explode_results.append(cls(sides, True))
            results = explode_results[:]

        if keep_drop:
            fn = keep_drop[0]
            number = int(keep_drop[1:])
            results.sort(key=lambda x: x.value)
            if fn == 'k':
                keep = results[-number:]
                drop = results[:-number]
                for d in drop: d.keep = False
                results = drop + keep
            elif fn == 'd':
                keep = results[:-number]
                drop = results[-number:]
                for d in drop: d.keep = False
                results = keep + drop
        return results

    @staticmethod
    def dice_roller(roll:str) -> (str, int):
        """Processes a dice roll string.

        Parameters
        ----------
        roll : :obj:`str`
            A dice roll string specification.
        
        Returns
        -------
        (:obj:`str`, :obj:`int`)
            A string that shows the results of the dice rolls and the total
            value of the rolls.
        
        """
        roll_exp = roll
        dice_rolls = re.findall(Die.DICE_REGEX, roll)
        dice_results = [Die.multi_roll(r) for r in dice_rolls]
        for i, r in enumerate(dice_rolls):
            str_result = '+'.join([str(d.value) for d in dice_results[i]])
            fstr_result = '+'.join([str(d) for d in dice_results[i]])
            str_result_disp = f'[{fstr_result}]'
            str_result_exp = f'({str_result})'
            roll = roll.replace(r, str_result_disp, 1)
            roll_exp = roll_exp.replace(r, str_result_exp, 1)
        
        result = utils.eval_expr(roll_exp)
        return roll, result

    @staticmethod
    def dice_sim(roll: str, n: int = 100000) -> Tuple[float, float, str]:
        """Simulate dice rolls repeatedly to collect statistics.

        Parameters
        ----------
        roll
            The dice roll specification.
        n
            Number of iterations to execute.

        """
        results = [Die.dice_roller(roll)[1] for _ in range(n)]
        r_min = min(results)
        r_max = max(results)
        mean = statistics.fmean(results)
        stdev = statistics.stdev(results)
        num_bins = (r_max - r_min) + 1
        fig, ax = plt.subplots()
        h_data, bins, patches = ax.hist(results, num_bins, density=True)

        ax.set_xlabel('Result')
        ax.set_ylabel('Probability Density')
        ax.set_title(f'Histogram of {roll} Rolled {n:,} Times')
        now = datetime.now()
        fname = f'/tmp/dbot_roll_sim_{now.strftime("%Y_%m_%d_%H_%M_%S")}.png'
        fig.tight_layout()
        fig.savefig(fname)
        logger.debug(fname)

        return mean, stdev, fname

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
        :obj:`int`
            The value of the roll.
        """
        self.__value =  random.choice(range(1, self.sides + 1))
        return self.__value
    
    @property
    def value(self) -> int:
        """The value of the last roll.

        Returns
        -------
        :obj:`int`
            The value of the last die roll.

        """
        return self.__value if self.keep else 0
    
    @property
    def critical_hit(self) -> bool:
        """Identifies if the last roll was a critical hit.

        Returns
        -------
        :obj:`bool`
            True if the last roll was a critical hit.

        """
        return self.__value == self.sides
    
    @property
    def critical_fail(self) -> bool:
        """Identifies if the last roll was a critical fail.

        Returns
        -------
        :obj:`bool`
            True if the last roll was a critical fail.
        
        """
        return self.__value == 1

def setup(bot: "Bot") -> None:
    """Add this :obj:`discord.ext.command.Cog` to the identified :obj:`discord.ext.command.Bot`.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The :obj:`discord.ext.command.Bot` that this :obj:`discord.ext.command.Cog`
        will be added to.
    
    """
    bot.add_cog(RollDice(bot))