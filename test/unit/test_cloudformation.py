import pytest
import cloudformation
from botocore.exceptions import ClientError


@pytest.fixture
def mock_cfn(mocker):
    mocker.patch.object(cloudformation, 'CFN')
    return cloudformation.CFN


def test_describe_stack_validation_error(mock_cfn):
    stack_name = 'myStack'
    exception_thrown = ClientError(
        {
            "Error": {
                "Code": "ValidationError"
            }
        },
        "DescribeStack"
    )
    mock_cfn.describe_stacks.side_effect = exception_thrown

    assert cloudformation.describe_stack(stack_name) is None
    mock_cfn.describe_stacks.assert_called_once_with(StackName=stack_name)


def test_describe_stack_other_error(mock_cfn):
    stack_name = 'myStack'
    exception_thrown = ClientError(
        {
            "Error": {
                "Code": "AccessDenied"
            }
        },
        "DescribeStack"
    )
    mock_cfn.describe_stacks.side_effect = exception_thrown

    with pytest.raises(ClientError):
        cloudformation.describe_stack(stack_name)
    mock_cfn.describe_stacks.assert_called_once_with(StackName=stack_name)


def test_describe_stack_empty_stacks(mock_cfn):
    stack_name = 'myStack'
    mock_cfn.describe_stacks.return_value = {'Stacks': []}

    assert cloudformation.describe_stack(stack_name) is None
    mock_cfn.describe_stacks.assert_called_once_with(StackName=stack_name)


def test_describe_stack_more_than_one_stack(mock_cfn):
    stack_name = 'myStack'
    stack = {'StackName': stack_name}
    mock_cfn.describe_stacks.return_value = {'Stacks': [stack, stack]}

    with pytest.raises(Exception):
        cloudformation.describe_stack(stack_name)
    mock_cfn.describe_stacks.assert_called_once_with(StackName=stack_name)


def test_describe_stack(mock_cfn):
    stack_name = 'myStack'
    stack = {'StackName': stack_name}
    mock_cfn.describe_stacks.return_value = {'Stacks': [stack]}

    assert cloudformation.describe_stack(stack_name) == stack
    mock_cfn.describe_stacks.assert_called_once_with(StackName=stack_name)


def test_wait_and_execute_change_set_failure(mock_cfn):
    change_set_id = 'change_set_id'
    mock_cfn.describe_change_set.return_value = {'Status': 'CREATE_FAILED'}

    with pytest.raises(Exception):
        cloudformation.wait_and_execute_change_set(change_set_id)
    mock_cfn.describe_change_set.assert_called_once_with(ChangeSetName=change_set_id)
    mock_cfn.execute_change_set.assert_not_called()


def test_wait_and_execute_change_set(mock_cfn):
    change_set_id = 'change_set_id'
    mock_cfn.describe_change_set.return_value = {'Status': 'CREATE_COMPLETE'}

    cloudformation.wait_and_execute_change_set(change_set_id)
    mock_cfn.describe_change_set.assert_called_once_with(ChangeSetName=change_set_id)
    mock_cfn.execute_change_set.assert_called_once_with(ChangeSetName=change_set_id)
