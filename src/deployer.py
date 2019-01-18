"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import lambdalogging
import config
import cloudformation
import repo
from distutils.version import LooseVersion

LOG = lambdalogging.getLogger(__name__)
REPO_STACK_PREFIX = 'serverlessrepo'
VALID_STACK_STATUS = ['CREATE_COMPLETE', 'UPDATE_COMPLETE', 'REVIEW_IN_PROGRESS', 'UPDATE_ROLLBACK_COMPLETE']


def handler(event, context):
    """Lambda function handler."""
    LOG.info('Received event: %s', event)

    stack_name = config.STACK_NAME
    application_id_in_stack, semantic_version = _get_application_from_stack(stack_name)
    application_id = config.APPLICATION_ID

    if application_id_in_stack is not None and application_id_in_stack != application_id:
        raise Exception('Stack %s is not created from application %s', stack_name, application_id)

    if not _has_newer_version(application_id, semantic_version):
        LOG.info('Current deployed version %s is the latest. No update is needed.', semantic_version)
        return

    LOG.info('Current deployed version %s is not the latest. Updating...', semantic_version)
    create_changeset_response = repo.create_change_set_with_template(application_id=application_id,
                                                                     stack_name=stack_name,
                                                                     parameter_overrides=config.PARAMETER_OVERRIDES,
                                                                     capabilities=config.CAPABILITIES)
    cloudformation.wait_and_execute_change_set(create_changeset_response['ChangeSetId'])


def _get_application_from_stack(stack_name):
    stack = cloudformation.describe_stack('-'.join([REPO_STACK_PREFIX, config.STACK_NAME]))
    if stack is None:
        LOG.info('Stack %s does not exist.', stack_name)
        return None, None
    if stack['StackStatus'] not in VALID_STACK_STATUS:
        raise Exception('Stack is not in a status that can be updated: %s', stack['StackStatus'])
    if 'Tags' not in stack:
        raise Exception('Stack %s is not created from an application in AWS Serverless Application Repository',
                        stack_name)
    LOG.info('Found stack %s', stack)
    tags = stack['Tags']
    application_id = None
    semantic_version = None
    for tag in tags:
        if tag['Key'] == 'serverlessrepo:applicationId':
            application_id = tag['Value']
        elif tag['Key'] == 'serverlessrepo:semanticVersion':
            semantic_version = tag['Value']

    if application_id is None or semantic_version is None:
        raise Exception('Stack %s does not have serverlessrepo:applicationId or serverlessrepo:semanticVersion in Tags',
                        stack_name)

    return application_id, semantic_version


def _has_newer_version(application_id, semantic_version):
    if semantic_version is None:
        return True

    get_application_response = repo.get_application(application_id)

    if 'Version' not in get_application_response:
        raise Exception('Application %s does not have a version to be deployed.', application_id)

    latest_semantic_version = get_application_response['Version']['SemanticVersion']
    LOG.info('Latest version of the application is %s', latest_semantic_version)
    return LooseVersion(latest_semantic_version) > semantic_version
