import pytest
import deployer
import test_constants


@pytest.fixture
def mock_repo(mocker):
    mocker.patch.object(deployer, 'repo')
    return deployer.repo


@pytest.fixture
def mock_cfn(mocker):
    mocker.patch.object(deployer, 'cloudformation')
    return deployer.cloudformation


def test_handler_stack_failed(mock_cfn):
    mock_cfn.describe_stack.return_value = {'StackStatus': 'UPDATE_FAILED'}

    with pytest.raises(Exception):
        deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))


def test_handler_stack_no_tag(mock_cfn):
    mock_cfn.describe_stack.return_value = {'StackStatus': 'UPDATE_COMPLETE'}

    with pytest.raises(Exception):
        deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))
