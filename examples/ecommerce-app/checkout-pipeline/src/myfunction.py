"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import lambdalogging

LOG = lambdalogging.getLogger(__name__)


def handler(event, context):
    """Lambda function handler."""
    LOG.info('Received event: {}', event)
