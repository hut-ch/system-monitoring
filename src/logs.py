"""logging helper functions"""

import logging
import os
import sys


def get_logger(
    name: str, log_file: str = "metrics.log", level=logging.INFO
) -> logging.Logger:
    """
    Returns a configured Logger with standardised formatting to stdout and log file
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)s \
| %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    log_path = create_log_file(log_file)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def create_log_file(log_file: str, path: str = "/logs/python"):
    """Create log file if it does not exist"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    log_path = os.path.join(path, log_file)

    try:
        with open(log_path, "a", encoding="utf-8"):
            return log_path
    except PermissionError as e:
        print(f"Error creating log file {log_file}: {e}")
        sys.exit(1)
