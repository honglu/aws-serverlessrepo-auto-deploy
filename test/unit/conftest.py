"""Setup unit test environment."""

import sys
import os

import test_constants

# make sure tests can import the app code
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../../src/')

# set expected config environment variables to test constants
os.environ['APPLICATION_ID'] = test_constants.APPLICATION_ID
os.environ['STACK_NAME'] = test_constants.STACK_NAME
os.environ['PARAMETER_OVERRIDES'] = test_constants.PARAMETER_OVERRIDES
os.environ['CAPABILITIES'] = test_constants.CAPABILITIES
