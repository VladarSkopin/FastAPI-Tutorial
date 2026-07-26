import logging
from logging.handlers import RotatingFileHandler


LOG_FORMAT = (
    "%(levelname)-8s "
    "%(asctime)s "
    "[ %(name)s ] "
    "%(message)s"
)

formatter = logging.Formatter(LOG_FORMAT)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
file_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        console_handler,
        file_handler,
    ],
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
