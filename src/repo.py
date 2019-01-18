"""Serverless Application Repository interfaces."""

import lambdalogging
import boto3
import time

REPO = boto3.client('serverlessrepo')
LOG = lambdalogging.getLogger(__name__)


def create_change_set_with_template(application_id, stack_name, parameter_overrides, capabilities):
    """
    Create CFN change set for application in AWS Serverless Application Repository.

    :param application_id: the application id to create change set for
    :param stack_name: the stack name
    :param parameter_overrides: parameter overrides
    :param capabilities: capabilities
    :return: change set id
    """
    LOG.info('Creating template for application %s', application_id)
    create_template_response = REPO.create_cloud_formation_template(ApplicationId=application_id)
    template_status = create_template_response['Status']
    template_id = create_template_response['TemplateId']
    while template_status != 'ACTIVE':
        LOG.info('Current template status for template id %s is %s', template_id, template_status)
        time.sleep(2)
        template_status = REPO.get_cloud_formation_template(ApplicationId=application_id,
                                                            TemplateId=template_id)['Status']
    LOG.info('Creating change set for stack %s with parameter %s and capabilities %s',
             stack_name, parameter_overrides, capabilities)
    return REPO.create_cloud_formation_change_set(ApplicationId=application_id,
                                                  TemplateId=template_id,
                                                  StackName=stack_name,
                                                  ParameterOverrides=parameter_overrides,
                                                  Capabilities=capabilities)


def get_application(application_id):
    """
    Get application.

    :param application_id: the application id
    :return: application
    """
    return REPO.get_application(ApplicationId=application_id)
