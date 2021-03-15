# -*- coding: utf-8 -*-
import logging
import pyparsing
import random
import re

from discord.ext import commands
from typing import List

import utils.basiceval

logger = logging.getLogger('dbot')

class RollDice(commands.Cog):
    """Dice rolling cog.

    Parameters
    ----------
    bot : :obj:`discord.ext.command.Bot`
        The controlling Bot.
    
    """

    def __init__(self, bot: "Bot"):
        self.bot = bot
        logger.info('RollDice Cog Loaded')
    
    @commands.command(aliases=['r'], help='Simulates rolling dice.')
    async def roll(self, ctx, *, dice_string: str = None) -> None:
        logger.info(f'Roll request from {ctx.author}')
        logger.info(f'    {dice_string}')
        try:
            results, total = Die.dice_roller(dice_string)
            await ctx.reply(f'{results} = {total}')
            logger.info(f'    Result: {results} = {total}')
        except pyparsing.ParseException as pe:
            response =  'Error in dice string at underline.'
            error_pos = dice_string[:pe.col-1] + f'__{dice_string[pe.col-1]}__' + dice_string[pe.col:]
            await ctx.reply(response + '\n' + error_pos)
            logger.error(response)
            logger.error(error_pos)

    @commands.command(help='More advanced information on a dice roll.')
    async def roll_help(self, ctx, *, ignore=None) -> None:
        help_str = """\
Dice rolls follow the form of <number of dice>d<number of sides> in a manner \
similar to the Roll20 specification. It also supports the basic math functions \
to add and subtract bonuses or multiply values.

Example: Roll a single D20.
>.roll 1d20
[18] = 18

Example: Roll two D8, add a bonus, and an additional D6 for extra damage.
>.roll 2d8+9+1d6
[1+5]+9+[4] = 19

Example: Roll the same damage roll as above but as a x3 critical.
>.roll 3\*(2d8+9+1d6)
3\*([6+4]+9+[**6**]) = 75

Additionally, the bot allows for the use of a '!' character at the end of each \
roll specification to identify exploding dice.

Example: Roll the same damage roll as above but allows for exploding dice rather \
than the x3 critical.
>.roll 2d8!+9+1d6!
[5+**8**+__2__]+9+[**6**+__5__] = 35 
"""
        await ctx.reply(help_str)

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
        self.roll

    DICE_REGEX = re.compile(r'(\d+d\d+[!]{0,1})')
    """:obj:`str` : A regex string find dice rolls in a larger string."""

    DICE_SPEC = re.compile(r'(\d+)d(\d+)([!]{0,1})')
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
        number_of_dice, number_of_sides, explode = \
            parsed[0] if parsed else (None, None, None)

        results = [cls(int(number_of_sides)) for _ in range(int(number_of_dice))]
        if explode == '!':
            explode_results = []
            for r in results:
                explode_results.append(r)
                while explode_results[-1].critical_hit:
                    explode_results.append(cls(int(number_of_sides), True))
            results = explode_results[:]

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
            result = utils.basiceval.basic_eval(roll_exp)

        return roll, utils.basiceval.basic_eval(roll_exp)

    def __str__(self):
        ret_val = str(self.value)
        if self.critical_hit or self.critical_fail:
            ret_val = f'**{ret_val}**'
        if self.exploded:
            ret_val = f'__{ret_val}__'
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
        return self.__value
    
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