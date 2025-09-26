from typing import Protocol
import logging


class SampleFilter(Protocol):
    """interface representing what filter objects have to
    implement to be used with the logger"""

    def filter(self, record: logging.LogRecord) -> bool:
        """determines if the log record should be passed to the handler

        Parameters:
        -----------
        record : logging.LogRecord
            value from program that gives runtime information. Commonly this is a
            string

        Returns:
        -------
        bool
            True or false indicating whether or not to pass the record to the
            handler
        """
        ...
