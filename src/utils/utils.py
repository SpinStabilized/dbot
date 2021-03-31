import logging
import logging.handlers
import math
import numexpr as ne
import os
import platform

from discord.ext import commands
from pathlib import Path
from typing import Final

DBOT_LOGGER_ID: Final[str] = 'dbot'
logger = logging.getLogger(DBOT_LOGGER_ID)

DBOT_LOG_FILE: Final[Path] = Path(f'logs/{DBOT_LOGGER_ID}.log')

def dbot_logger_config(level: int = logging.INFO) -> logging.Logger:
    """Configure the DBot's logger

    Provides a logger that outputs to both the console and to a log
    file. The log file is configured to rotate every night at midnight.

    Parameters
    ----------
    level
        The debugging level, should probably use constants from the
        `logging` module.
    
    """
    host: str = platform.node()
    logger: logging.Logger = logging.getLogger(DBOT_LOGGER_ID)
    logger.setLevel(level)
    log_format = logging.Formatter(
                    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_dir = DBOT_LOG_FILE.parents[0]
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.TimedRotatingFileHandler(
                        filename=str(DBOT_LOG_FILE),
                        encoding='utf-8',
                        when='midnight',
                        backupCount=10
    )
    file_handler.setFormatter(log_format)
    console_handler: logging.handlers.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

def get_dbot_logger() -> logging.Logger:
    """Grab a DBot Logger

    """
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

def eval_expr(expr:str='0') -> float:
    """Evaluate a string as a math expression.

    Parameters
    ----------
    expr
        An expression, as a :class:`str`, to evaluate.
    
    """
    pi = math.pi
    e = math.pi
    tau = math.tau

    result = ne.evaluate(expr).item()
    return result

