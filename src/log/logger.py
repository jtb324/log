import logging
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, Union

# We are going to configure a specific logging level for
# VERBOSE versus INFO
logging.VERBOSE = logging.INFO - 5


class LoggerOpts:

    def __init__(self, to_console: bool = False, verbosity: int = 0) -> None:
        self.to_console = to_console
        self.verbosity = verbosity


class HandlerOpts:

    def __init__(
        self,
        filename: str = "test.log",
        output_dir: Path = Path("./"),
        rotate_handle: bool = False,
        max_size: int = 1024,
        backup_filecount: int = 5,
    ) -> None:
        """container for all of the options that get passed to the handler

        Parameters
        ----------
        filename : str
            the name of the output file. This value is just the name not
            the full path including the directory. Default value: test.log

        output_dir : Path
            path to the output directory that the log will be written to.
            Default value: Path("./")

        rotate_handle : bool
            whether or not to use a rotatingFileHandle. If true then the
            logger will close the existing filehandle and start a new one
            once the file gets to be a  certain size. Default value: False

        max_size : int
            max_size for the log file to be before the logger will close the
            file and start logging to a new file. Values are in bytes. Default
            value: 1024

        backup_filecount: int
            number of log files to keep as backups. If the program reaches the
            backup_filecount then it deletes the oldest log. Default value: 5
        Raises
        ------
        ValueError
            if the output directory doesn't exist then the program throws
            a ValueError
        """
        self.filename = filename
        if not output_dir.exists():
            raise ValueError(f"The directory {output_dir} was not found")
        self.output_dir = output_dir
        self.use_rotating_handle = rotate_handle
        self.max_size = max_size
        self.backup_filecount = backup_filecount


class FormatterOpts:

    def __init__(self) -> None:
        self.format_strings: Dict[str, str | None] = {
            "file_format": None,
            "stream_format": None,
        }

    def add_format(self, format_str: str, handler_name: str) -> None:
        """add the formatting string to the FormatterOpts

        Parameters
        ----------
        format_str : str
            string that will be passed to the handler to indicate how
            the log file should write the record

        handler_name : str
            which handler the formatter string should go to. Allowed values are 'file' or 'stream'

        Raises
        ------
        ValueError
            if the handler name is not one of the allowed values then the program throws a ValueError
            that informs the user what the allowed values are
        """
        if handler_name not in ["file", "stream"]:
            raise ValueError(
                f"Unrecognized handler name: {handler_name}. Allowed values are 'file' or 'stream'"
            )

        match handler_name:
            case "file":
                self.format_strings["file_format"] = format_str
            case "stream":
                self.format_strings["stream"] = format_str


class CustomLogger(logging.getLoggerClass()):
    def __init__(self, name: str, level: int = logging.NOTSET) -> None:
        """Initialize the CustomLogger class

        Parameters
        ----------
        name : str
            name of the logger. could be __main__

        level : int
            log level represented as an integer
        """
        super().__init__(name, level)
        # we want a default verbosity level of 15

        logging.addLevelName(logging.VERBOSE, "VERBOSE")

    def verbose(self, msg, *args, **kwargs) -> None:
        """log messages at a verbose level

        Parameters
        ----------
        msg : str
            message provided to the logger
        """
        if self.isEnabledFor(logging.VERBOSE):
            self._log(logging.VERBOSE, msg, args, **kwargs)

    def record_namespace(self, inputs: Namespace) -> None:
        """log the user arguments from the argparse Namespace

        Parameters
        ----------
        inputs : Namespace
            Namespace object that has all of the arguments passed to Argparse parser
        """
        argument_dictionary = vars(inputs)

        current_level = self.getEffectiveLevel()
        # changing the loglevel so that it records the info messages here
        self.setLevel(logging.INFO)

        self.info("Program Arguments in NameSpace:")
        self.info(f"{'~' * 30}")
        # going over each value in the kwargs to write to a file
        for parameter, value in argument_dictionary.items():
            self.info(f"{parameter}: {value}")

        self.info(f"{'~' * 30}")
        self.info("\n")
        # getting the correct log level to reset the logger
        self.setLevel(current_level)

    def record_inputs(self, **kwargs: Dict[str, Any]) -> None:
        """function to record the user arguments that were passed to the
        program. Takes a logger and then a dictionary of the user
        arguments

        Parameters
        ----------
        logger : logging.Logger"""

        current_level = self.getEffectiveLevel()
        # changing the loglevel so that it records the info messages here
        self.setLevel(logging.INFO)

        # going over each value in the kwargs to write to a file
        for parameter, value in kwargs.items():
            self.info(f"{parameter}: {value}")

        # getting the correct log level to reset the logger
        self.setLevel(current_level)

    @staticmethod
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
        if loglevel == 0:
            return logging.INFO
        elif loglevel == 1:
            return logging.VERBOSE
        else:
            return logging.DEBUG

    def configure(
        self,
        handlerOpts: HandlerOpts,
        loggerOpts: LoggerOpts,
        formatterOpts: FormatterOpts,
        format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ) -> None:
        """Function that will configure the logger

        Parameters
        ----------
        logger"""
        if (
            handlerOpts.filename is None
        ):  # If there is no filename provided then we are going to assume that the user only wants to write to STDOUT
            to_console = True

        if handlerOpts.filename:
            filename = handlerOpts.output_dir / handlerOpts.filename

            self.setLevel(CustomLogger.get_loglevel(loggerOpts.verbosity))

            file_formatter = logging.Formatter(format_str)

            # program defaults to log to a file called IBDCluster.log in the
            # output directory
            fh = logging.FileHandler(filename, mode="w")
            fh.setFormatter(file_formatter)
            self.addHandler(fh)

        # If the user selects to also log to console then the program will
        # log information to the stderr
        if loggerOpts.to_console:
            stream_formatter = logging.Formatter("%(message)s")

            sh = logging.StreamHandler()
            sh.setFormatter(stream_formatter)
            self.addHandler(sh)

    @staticmethod
    def get_logger(module_name: str, main_name: str = "__main__") -> logging.Logger:
        """Function that will be responsible for getting the logger for modules"""
        return logging.getLogger(main_name).getChild(module_name)

    @staticmethod
    def create_logger(
        logger_name: str = "__main__",
    ) -> logging.Logger:
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


logging.setLoggerClass(CustomLogger)
