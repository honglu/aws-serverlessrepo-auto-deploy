import pytest
import repo


@pytest.fixture
def mock_repo(mocker):
    mocker.patch.object(repo, 'REPO')
    return repo.REPO


def test_get_application(mock_repo):
    app_id = 'myApp'
    app = {'ApplicationId': app_id}
    mock_repo.get_application.return_value = app

    assert repo.get_application(app_id) == app
    mock_repo.get_application.assert_called_once_with(ApplicationId=app_id)


def test_create_change_set_with_template(mock_repo):
    app_id = 'myApp'
    stack_name = 'myStack'
    parameter_overrides = [{'Name': 'MyParam', 'Value': 1}]
    capabilities = ['CAPABILITY_IAM']
    template_id = 'myTemplateId'
    mock_repo.create_cloud_formation_template.return_value = {'Status': 'PREPARING', 'TemplateId': template_id}
    mock_repo.get_cloud_formation_template.return_value = {'Status': 'ACTIVE'}

    repo.create_change_set_with_template(app_id, stack_name, parameter_overrides, capabilities)
    mock_repo.create_cloud_formation_template.assert_called_once_with(ApplicationId=app_id)
    mock_repo.get_cloud_formation_template.assert_called_once_with(ApplicationId=app_id, TemplateId=template_id)
