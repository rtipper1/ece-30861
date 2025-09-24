# src/logging_config.py
import logging, os

def setup_logger():
    log_file = os.getenv("LOG_FILE", "app.log")
    log_level_str = os.getenv("LOG_LEVEL", "0")

    try:
        log_level = int(log_level_str)
    except ValueError:
        log_level = 0

    if log_level == 0:
        level = logging.CRITICAL
    elif log_level == 1:
        level = logging.INFO
    elif log_level == 2:
        level = logging.DEBUG
    else:
        level = logging.CRITICAL

    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s : %(levelname)s : %(message)s"
    )

    return logging.getLogger("metric_logger")
