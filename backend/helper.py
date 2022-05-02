# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import sys

"""
AK8PO: Helper functions

@author: Filip Findura
"""


def set_logging(name: str, level: str) -> log.Logger:
    """Set up attributes of the root logger

    :param name: string name of the logger
    :param level: string name of base log level
    """
    log_format = "%(asctime)s | %(levelname)-5s | %(message)s"
    if level == "DEBUG":
        log_format += " | %(filename)s@ln%(lineno)d"
    formatter = log.Formatter(log_format)

    logger = log.getLogger(name)
    logger.setLevel(level)
    handler = log.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def degrees_to_direction(deg: int) -> str:
    if deg > 348:
        compass = "N"
    elif deg > 326:
        compass = "NNW"
    elif deg > 304:
        compass = "NW"
    elif deg > 281:
        compass = "WNW"
    elif deg > 258:
        compass = "W"
    elif deg > 236:
        compass = "WSW"
    elif deg > 214:
        compass = "SW"
    elif deg > 191:
        compass = "SSW"
    elif deg > 169:
        compass = "S"
    elif deg > 146:
        compass = "SSE"
    elif deg > 124:
        compass = "SE"
    elif deg > 101:
        compass = "ESE"
    elif deg > 78:
        compass = "E"
    elif deg > 56:
        compass = "ENE"
    elif deg > 34:
        compass = "NE"
    elif deg > 11:
        compass = "NNE"
    else:
        compass = "N"

    return compass
