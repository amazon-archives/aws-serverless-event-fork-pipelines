"""Lambda logging helper.

Returns a Logger with log level set based on env variables.
"""

import logging

import config

# translate log level from string to numeric value
LOG_LEVEL = getattr(logging, config.LOG_LEVEL) if hasattr(logging, config.LOG_LEVEL) else logging.INFO


def getLogger(name):
    """Return a logger configured based on env variables."""
    logger = logging.getLogger(name)
    # in lambda environment, logging config has already been setup so can't use logging.basicConfig to change log level
    logger.setLevel(LOG_LEVEL)
    return logger
