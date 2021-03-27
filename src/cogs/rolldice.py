# -*- coding: utf-8 -*-
import logging
import pyparsing
import random
import re

from discord.ext import commands
from typing import List

import utils

logger = utils.get_dbot_logger()

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
            async with ctx.typing():
                results, total = Die.dice_roller(dice_string)
                await ctx.reply(f'{results} = {total}')
                logger.info(f'    Result: {results} = {total}')
        except pyparsing.ParseException as pe:
            response =  'Error in dice string at underline.'
            logger.error(pe)
            error_pos = dice_string[:pe.col-1] + f'__{dice_string[pe.col-1]}__' + dice_string[pe.col:]
            await ctx.reply(response + '\n' + error_pos)
            logger.error(response)
            logger.error(error_pos)


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
        
        result = utils.basic_eval(roll_exp)
        return roll, result

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