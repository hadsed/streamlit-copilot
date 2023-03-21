import os
import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler


def add_file_handler(
    logger: logging.Logger,
    formatter: logging.Formatter,
    file_name: str,
    base_dir: str,
) -> None:
    file_path = os.path.join(base_dir, file_name)
    file_handler = RotatingFileHandler(file_path, maxBytes=1e6, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def configure_stream_logger(logger: logging.Logger, log_level: str) -> None:
    logger.setLevel(log_level)
    logger.propagate = False
    has_a_stream_handler = any(
        isinstance(h, logging.StreamHandler) for h in logger.handlers)
    rich_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_path=True,
        log_time_format="%y-%m-%d %H:%M:%S")
    if not has_a_stream_handler:
        logger.addHandler(rich_handler)
