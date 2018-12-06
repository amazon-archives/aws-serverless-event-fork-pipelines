"""Environment configuration values used by lambda functions."""

import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
TABLE_NAME = os.getenv('TABLE_NAME')
