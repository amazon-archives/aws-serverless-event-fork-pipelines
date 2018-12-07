"""Environment configuration values used by lambda functions."""

import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
TOPIC_ARN = os.getenv('TOPIC_ARN')
