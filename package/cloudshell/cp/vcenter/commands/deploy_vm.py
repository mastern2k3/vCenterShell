﻿from cloudshell.cp.vcenter.models.DeployFromTemplateDetails import DeployFromTemplateDetails


class DeployCommand(object):
    """ Command to Create a VM from a template """

    def __init__(self, deployer):
        """
        :param deployer:   pv_service Instance
        :type deployer:   cloudshell.cp.vcenter.vm.deploy.VirtualMachineDeployer
        """
        self.deployer = deployer

    def execute_deploy_from_template(self, si, deployment_params, resource_context, logger):
        """

        :param si:
        :type deployment_params: DeployFromTemplateDetails
        :param resource_context:
        :param logger:
        :return:
        """
        deploy_result = self.deployer.deploy_from_template(si, deployment_params, resource_context, logger)
        return deploy_result

    def execute_deploy_from_image(self, si, session, vcenter_data_model, deployment_params, resource_context, logger):
        """

        :param si:
        :param session:
        :param vcenter_data_model:
        :param deployment_params:
        :param resource_context:
        :param logger:
        :return:
        """
        deploy_result = self.deployer.deploy_from_image(si=si,
                                                        session=session,
                                                        vcenter_data_model=vcenter_data_model,
                                                        data_holder=deployment_params,
                                                        resource_context=resource_context,
                                                        logger=logger)
        return deploy_result
