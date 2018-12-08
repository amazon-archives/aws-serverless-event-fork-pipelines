"""Environment configuration values used by lambda functions."""

import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
FIREHOSE_DELIVERY_STREAM_NAME = os.getenv('FIREHOSE_DELIVERY_STREAM_NAME')
