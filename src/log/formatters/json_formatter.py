import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        """formats the log record as a json object

        Parameters
        ----------
        record : loggig.LogRecord
            message to be sent to the logger

        Returns
        -------
        str
            returns the formatted json object as a string
        """
        formatted_log = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "loglevel": record.levelname,
            "logger_name": record.name,
        }
        return json.dumps(formatted_log)
