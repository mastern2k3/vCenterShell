from cloudshell.cp.vcenter.commands.cloudshell_session_factory import ContextBasedService
from cloudshell.cp.vcenter.models.VMwarevCenterResourceModel import VMwarevCenterResourceModel
from pyVim.connect import SmartConnect, Disconnect
from cloudshell.cp.vcenter.common.vcenter.vmomi_service import pyVmomiService


class VCenterOperationContext(ContextBasedService):
    def __init__(self, session, vcenter_resource_model, resource_context):
        self.session = session
        self.vcenter_resource_model = vcenter_resource_model
        self.resource_context = resource_context
        self.pv_service = pyVmomiService(SmartConnect, Disconnect)

    def context_started(self):
        user = self.vcenter_resource_model.user
        encrypted_pass = self.vcenter_resource_model.password
        vcenter_url = self.resource_context.address
        password = self.session.DecryptPassword(encrypted_pass).Value

        self.si = self.pv_service.connect(vcenter_url, user, password, 443)
        return self.si

    def context_ended(self):
        self.pv_service.disconnect(self.si)

    def get_objects(self):
        return self.si


class VCenterOperationContextFactory(object):
    def __init__(self, resource_model_parser):
        self.resource_model_parser = resource_model_parser

    def create_vcenter_session(self, session, context):
        vcenter_data_model = self._create_vcenter_resource_model(context)
        return VCenterOperationContext(session, vcenter_data_model, context)

    def _create_vcenter_resource_model(self, context):
        return self.resource_model_parser.convert_to_resource_model(
            resource_instance=context.resource,
            resource_model_type=VMwarevCenterResourceModel)

