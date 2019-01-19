"""CloudFormation interfaces."""

import lambdalogging
import boto3
from botocore.exceptions import ClientError

CFN = boto3.client('cloudformation')
LOG = lambdalogging.getLogger(__name__)
CHANGE_SET_IN_PROGRESS_STATUS = ['CREATE_PENDING', 'CREATE_IN_PROGRESS']


def wait_and_execute_change_set(change_set_id):
    """
    Wait for the CFN change set to become CREATE_COMPLETE and then execute the change set.

    :param change_set_id: the ID of the change set
    """
    while True:
        change_set_status = CFN.describe_change_set(ChangeSetName=change_set_id)['Status']
        LOG.info("Current change set status for change set id %s is %s", change_set_id, change_set_status)
        if change_set_status == 'CREATE_COMPLETE':
            break
        if change_set_status not in CHANGE_SET_IN_PROGRESS_STATUS:
            raise Exception('ChangeSet %s is not in desired status: %s', change_set_id, change_set_status)

    LOG.info("Executing change set %s", change_set_id)
    CFN.execute_change_set(ChangeSetName=change_set_id)


def describe_stack(stack_name):
    """
    Describe a stack.

    :param stack_name: the stack name
    :return: stack
    """
    try:
        stacks = CFN.describe_stacks(StackName=stack_name)['Stacks']
    except ClientError as e:
        if e.response['Error']['Code'] == 'ValidationError':
            return None
        else:
            raise e

    if not stacks:
        return None
    elif len(stacks) > 1:
        raise Exception('There are more than one stack with name %s', stack_name)
    return stacks[0]
