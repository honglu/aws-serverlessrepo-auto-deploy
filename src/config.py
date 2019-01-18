"""Environment configuration values used by lambda functions."""

import os
import json

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
APPLICATION_ID = os.getenv('APPLICATION_ID')
STACK_NAME = os.getenv('STACK_NAME')
PARAMETER_OVERRIDES = [] if os.getenv('PARAMETER_OVERRIDES') == '' else json.loads(os.getenv('PARAMETER_OVERRIDES'))
CAPABILITIES = [] if os.getenv('CAPABILITIES') == '' else json.loads(os.getenv('CAPABILITIES'))
