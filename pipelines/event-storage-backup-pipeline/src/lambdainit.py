"""Special initializations for Lambda functions.

This file must be imported as the first import in any file containing a Lambda function handler method.
"""

import sys

# add packaged dependencies to search path
sys.path.append('lib')

# imports of library dependencies must come after setting up the dependency search path
from aws_xray_sdk.core import patch_all  # noqa: E402

# patch all supported libraries for X-Ray tracing
patch_all()
