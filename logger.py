import logging
import os
from pathlib import Path
from typing import Dict

level_dict: Dict[int, int] = {
    1: logging.DEBUG,
    2: logging.INFO,
}


def record_inputs(logger, **kwargs) -> None:
    """function to record the user arguments that were passed to the
    program. Takes a logger and then a dictionary of the user
    arguments"""

    logger.setLevel(20)

    for parameter, value in kwargs.items():
        logger.info(f"{parameter}: {value}")

    # getting the correct log level to reset the logger
    logger.setLevel(get_loglevel(kwargs["loglevel"]))


def get_loglevel(loglevel: int) -> int:
    """Function that will return a log level based on the input

    Parameters
    ----------
    loglevel : int
        integer that represents what loglevel the program
        will use. This number will be zero if the user didn't
        pass the verbose flag and will be 1 if the user
        passed the verbose flag.

    Returns
    -------
    int
        returns an integer representing the loglevel in the level_dict
    """

    return level_dict.get(loglevel, logging.INFO)


def configure(
    logger: logging.Logger,
    output: Path,
    filename: str = "IBDCluster.log",
    loglevel: int = 0,
    to_console: bool = False,
    format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> None:
    """Function that will configure the level of logging"""

    filename = output / filename

    logger.setLevel(level_dict.get(loglevel, logging.INFO))

    file_formatter = logging.Formatter(format_str)

    # program defaults to log to a file called IBDCluster.log in the
    # output directory
    fh = logging.FileHandler(filename, mode="w")
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)

    # If the user selects to also log to console then the program will
    # log information to the stderr
    if to_console:
        stream_formatter = logging.Formatter("%(message)s")

        sh = logging.StreamHandler()
        sh.setFormatter(stream_formatter)
        logger.addHandler(sh)


def get_logger(module_name: str, main_name: str = "__main__") -> logging.Logger:
    """Function that will be responsible for getting the logger for modules"""
    return logging.getLogger(main_name).getChild(module_name)


def create_logger(logger_name: str = "__main__",) -> logging.Logger:
    """Function that will get the correct logger for the program

    Parameters
    ----------
    loglevel : str
        logging level that the user wants to use. The default level is INFO

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(logger_name)

    return logger
