# This filter will allow us to sample only a proportion of logs
# passed from the logger to the handler
import logging
import random

from log.sampling_filters.filter_interface import SampleFilter

# We are going to configure a specific logging level for
# VERBOSE versus INFO
logging.VERBOSE = logging.INFO - 5


class RandomPropFilter(SampleFilter):
    """filter on a proportion of log messages"""

    def __init__(self, proportion: float, loglevel: int | None = None) -> None:
        """
        Parameters:
        -----------
        proportion : float
            proportion of log messages to keep. For example if the value is 0.1
            and there are 1000 messages than ~100 messages should be kept. There
            is randomness in the method which is why the value of records kept is
            approximate

        loglevel : int | None
            integer representing what severity of messages to keep. This value can
            be an integer but it is better to use the python enum logger.INFO,
            logging.DEBUG, etc.. Values including and below this log level will be
            sampled.

        Raises:
        -------
        ValueError:
            if the proportion is < 0 or > 1, then we raise an error because these
            values don't make sens
        """
        if proportion > 1 or proportion < 0:
            raise ValueError(
                f"Expected the proportion of log records to keep to be between (inclusively) 0,1. Instead the value of {proportion} was passed to the ProportionFilter"
            )
        self.proportion = proportion

        if (
            loglevel is not None
            and isinstance(loglevel, int)
            and logging.getLevelName(loglevel).startswith("level")
        ):
            raise ValueError(
                f"Expected a valid loglevel or {logging.INFO}, {logging.VERBOSE}, {logging.DEBUG}, {logging.FATAL}. Received a value of {loglevel}"
            )
        self.loglevel = loglevel

    def filter(self, record: logging.LogRecord) -> bool:
        """randomly sample logs based on a proportion of logs to keep.

        Parameters:
        -----------
        record : logging.LogRecord
            message about program runtime passed from the logger

        Returns:
        --------
        bool
            boolean indicating whether to keep the record. This will
            indicate if the value should be passed to the handler
        """
        # Here are the cases we need to account for:
        # 1. User wants to return all records (1st if statement)
        # 2. User wants sampling applied to all records (elif)
        # 3. User wants sampling applied to only certain log
        #    levels (else statement)
        if self.proportion == 1:
            return True
        elif self.loglevel is None:
            return random.random() <= self.proportion
        else:
            if record.levelno <= self.loglevel:
                return random.random() <= self.proportion
            else:
                return True
