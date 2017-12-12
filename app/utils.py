import os
import logging
from time import sleep
from logging.handlers import RotatingFileHandler
from collections import namedtuple


OffsetIteration = namedtuple("OffsetIteration", ["offset", "count"])


def offset_range(total, count_max, offset=0):
    if total <= 0:
        raise ValueError("total must be pos int")
    if count_max <= 0:
        raise ValueError("count_max must be pos int")

    while total:
        if total < count_max:
            count_cur = total
        else:
            count_cur = count_max
        yield OffsetIteration(offset, count_cur)
        total -= count_cur
        offset += count_cur


def rate_limit_sleep_hook(seconds):
    def hook(response, **kwargs):
        sleep(seconds)
    return hook


def configure_logging(app):
    # Log path
    if not os.path.exists(app.config["LOG_DIR"]):
        os.mkdir(app.config["LOG_DIR"])

    # Logger log level
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # Handler
    handler = RotatingFileHandler(
        filename=app.config["LOG_PATH"],
        mode="a",
        maxBytes=app.config["LOG_MAX_BYTES"],
        backupCount=app.config["LOG_BAK_COUNT"]
    )
    handler.setFormatter(logging.Formatter(app.config["LOG_FMT"]))
    handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    app.logger.addHandler(handler)
