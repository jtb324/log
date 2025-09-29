import logging
import json


class JsonFormatter(logging.Formatter):

    def __init__(self) -> None:
        super().__init__()
        self._record_keys = logging.LogRecord(
            "", 0, "", 0, "", (), None
        ).__dict__.keys()

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
            "timestamp": record.asctime,
            "loglevel": record.levelname,
            "logger_name": record.name,
            "filepath": record.pathname,
            "function_call": record.funcName,
            "line_number": record.lineno,
            "message": record.getMessage(),
            "context": {},  # This value is purely going to hold additional context for the program
            "exception": "",
        }

        # Add key values for context if an LoggerAdapter was used.
        for key, value in record.__dict__.items():
            if key not in self._record_keys:
                formatted_log["context"][key] = value

        if record.exc_info:
            formatted_log["exception"] = self.formatException(record.exc_info)

        return json.dumps(formatted_log)
