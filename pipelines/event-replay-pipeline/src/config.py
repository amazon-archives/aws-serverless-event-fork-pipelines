"""Environment configuration values used by lambda functions."""

import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DESTINATION_SQS_QUEUE_NAME = os.getenv('DESTINATION_SQS_QUEUE_NAME')
