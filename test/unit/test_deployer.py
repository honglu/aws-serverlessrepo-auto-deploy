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


def test_handler_stack_no_application_id_in_tag(mock_cfn):
    mock_cfn.describe_stack.return_value = {
        'StackStatus': 'CREATE_COMPLETE',
        'Tags': [{
            'Key': 'serverlessrepo:semanticVersion',
            'Value': '1.0.0'
        }]
    }

    with pytest.raises(Exception):
        deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))


def test_handler_stack_no_semantic_version_in_tag(mock_cfn):
    mock_cfn.describe_stack.return_value = {
        'StackStatus': 'CREATE_COMPLETE',
        'Tags': [{
            'Key': 'serverlessrepo:applicationId',
            'Value': test_constants.APPLICATION_ID
        }]
    }

    with pytest.raises(Exception):
        deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))


def test_handler_stack_application_id_not_match(mock_cfn):
    mock_cfn.describe_stack.return_value = {
        'StackStatus': 'CREATE_COMPLETE',
        'Tags': [
            {
                'Key': 'serverlessrepo:applicationId',
                'Value': 'not match'
            },
            {
                'Key': 'serverlessrepo:semanticVersion',
                'Value': '1.0.0'
            }
        ]
    }

    with pytest.raises(Exception):
        deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))


def test_handler_stack_no_version(mock_cfn, mock_repo):
    mock_cfn.describe_stack.return_value = {
        'StackStatus': 'CREATE_COMPLETE',
        'Tags': [
            {
                'Key': 'serverlessrepo:applicationId',
                'Value': test_constants.APPLICATION_ID
            },
            {
                'Key': 'serverlessrepo:semanticVersion',
                'Value': '1.0.0'
            }
        ]
    }
    mock_repo.get_application.return_value = {}

    with pytest.raises(Exception):
        deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))
    mock_repo.get_application.assert_called_once_with(test_constants.APPLICATION_ID)
    mock_repo.create_change_set_with_template.assert_not_called()


def test_handler_stack_no_newer_version(mock_cfn, mock_repo):
    mock_cfn.describe_stack.return_value = {
        'StackStatus': 'CREATE_COMPLETE',
        'Tags': [
            {
                'Key': 'serverlessrepo:applicationId',
                'Value': test_constants.APPLICATION_ID
            },
            {
                'Key': 'serverlessrepo:semanticVersion',
                'Value': '1.0.0'
            }
        ]
    }
    mock_repo.get_application.return_value = {'Version': {'SemanticVersion': '0.0.1'}}

    deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))
    mock_repo.get_application.assert_called_once_with(test_constants.APPLICATION_ID)
    mock_repo.create_change_set_with_template.assert_not_called()
    mock_repo.create_change_set_with_template.assert_not_called()


def test_handler(mock_cfn, mock_repo):
    change_set_id = 'myChangeSet'
    mock_cfn.describe_stack.return_value = {
        'StackStatus': 'CREATE_COMPLETE',
        'Tags': [
            {
                'Key': 'serverlessrepo:applicationId',
                'Value': test_constants.APPLICATION_ID
            },
            {
                'Key': 'serverlessrepo:semanticVersion',
                'Value': '1.0.0'
            }
        ]
    }
    mock_repo.get_application.return_value = {'Version': {'SemanticVersion': '1.0.1'}}
    mock_repo.create_change_set_with_template.return_value = {'ChangeSetId': change_set_id}

    deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))
    mock_repo.get_application.assert_called_once_with(test_constants.APPLICATION_ID)
    mock_repo.create_change_set_with_template.assert_called_once_with(
        application_id=test_constants.APPLICATION_ID,
        stack_name=test_constants.STACK_NAME,
        parameter_overrides={"Name": "myParam", "Value": 1},
        capabilities=["CAPABILITY_IAM"])
    mock_cfn.wait_and_execute_change_set.assert_called_once_with(change_set_id)


def test_handler_new_stack(mock_cfn, mock_repo):
    change_set_id = 'myChangeSet'
    mock_cfn.describe_stack.return_value = None
    mock_repo.create_change_set_with_template.return_value = {'ChangeSetId': change_set_id}

    deployer.handler({}, None)
    mock_cfn.describe_stack.assert_called_once_with("serverlessrepo-{}".format(test_constants.STACK_NAME))
    mock_repo.get_application.assert_not_called()
    mock_repo.create_change_set_with_template.assert_called_once_with(
        application_id=test_constants.APPLICATION_ID,
        stack_name=test_constants.STACK_NAME,
        parameter_overrides={"Name": "myParam", "Value": 1},
        capabilities=["CAPABILITY_IAM"])
    mock_cfn.wait_and_execute_change_set.assert_called_once_with(change_set_id)
