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
