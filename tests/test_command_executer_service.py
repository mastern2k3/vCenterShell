import unittest
from mock import MagicMock, Mock
from utils.command_context_mocker import CommandContextMocker
from utils.vm_context import VmContext
from vCenterShell.command_executer import CommandExecuterService


class TestCommandExecuterService(unittest.TestCase):
    def setUp(self):
        self.serializer = Mock()
        self.connection_retriever = Mock()
        self.connection_details = Mock()
        self.command_wrapper = Mock()
        self.connection_retriever.connection_details = Mock(return_value=self.connection_details)
        self.quali_helpers = Mock()
        connection_details, connection_retriever = self.create_connection_ret_mock()
        self.connection_retriever = connection_retriever
        self.connection_details = connection_details

    def create_connection_ret_mock(self):
        vcenter_name = 'vcenter name'
        connection_retriever = Mock()
        connection_details = Mock()
        connection_retriever.getVCenterInventoryPathAttributeData = \
            Mock(return_value={'vCenter_resource_name': vcenter_name})
        connection_retriever.connection_details = Mock(return_value=connection_details)
        return connection_details, connection_retriever

    def test_deploy_from_template(self):
        # arrange
        deploy_param = 'deploy_param'
        deploy_data = {'mock': Mock()}
        deploy_result = Mock()

        self.quali_helpers.get_user_param = Mock(return_value=deploy_param)
        self.serializer.decode = Mock(return_value=deploy_data)
        self.serializer.encode = Mock(return_value=True)
        self.command_wrapper.execute_command_with_connection = Mock(return_value=deploy_result)

        deploy_from_template = Mock()
        deploy_from_template.deploy_execute = Mock(return_value=True)

        command_executer_service = CommandExecuterService(Mock(),
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          deploy_from_template,
                                                          Mock(),
                                                          Mock(),
                                                          Mock())

        # act
        command_executer_service.deploy_from_template()

        # assert
        self.assertTrue(self.quali_helpers.get_user_param.called_with('DEPLOY_DATA'))
        self.assertTrue(self.serializer.decode.called_with(deploy_param))
        self.assertTrue(self.connection_retriever.connection_details.called)
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(
            self.connection_details,
            deploy_from_template.execute_deploy_from_template,
            deploy_data))
        self.assertTrue(self.serializer.encode.called_with(deploy_result))

    def test_power_off(self):
        # arrange
        resource_att = Mock()
        power_manager = Mock()

        self.quali_helpers.get_resource_context_details = Mock(return_value=resource_att)
        power_manager.power_off = Mock(return_value=True)

        command_executer_service = CommandExecuterService(Mock(),
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          power_manager,
                                                          Mock())

        CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)

        # act
        command_executer_service.power_off()

        # assert
        self.assertTrue(self.connection_retriever.getVCenterInventoryPathAttributeData.called_with(resource_att))
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(self.connection_details,
                                                                                         power_manager.power_off,
                                                                                         VmContext.VM_UUID))

    def test_power_on(self):
        # arrange
        resource_att = Mock()
        power_manager = Mock()

        self.quali_helpers.get_resource_context_details = Mock(return_value=resource_att)
        power_manager.power_off = Mock(return_value=True)

        command_executer_service = CommandExecuterService(Mock(),
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          power_manager,
                                                          Mock())

        CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)

        # act
        command_executer_service.power_on()

        # assert
        self.assertTrue(self.connection_retriever.getVCenterInventoryPathAttributeData.called_with(resource_att))
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(self.connection_details,
                                                                                         power_manager.power_on,
                                                                                         VmContext.VM_UUID))

    def test_destroyVirtualMachineCommand(self):
        # arrange
        resource_att = Mock()
        Destroyer = Mock()
        self.quali_helpers.get_resource_context_details = Mock(return_value=resource_att)
        Destroyer.power_off = Mock(return_value=True)

        command_executer_service = CommandExecuterService(Mock(),
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Destroyer,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          Mock())

        CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)

        # act
        command_executer_service.destroy()

        # assert
        self.assertTrue(self.connection_retriever.getVCenterInventoryPathAttributeData.called_with(resource_att))
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(self.connection_details,
                                                                                         Destroyer.destroy,
                                                                                         VmContext.VM_UUID,
                                                                                         resource_att.fullname))

    def test_disconnect(self):
        # arrange
        virtual_switch_disconnect_command = Mock()
        virtual_switch_disconnect_command.disconnect_all = Mock(return_value=True)
        command_executer_service = CommandExecuterService(Mock(),
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          virtual_switch_disconnect_command,
                                                          Mock())

        CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)
        CommandContextMocker.set_vm_uuid_param(VmContext.NETWORK_NAME)

        # act
        command_executer_service.disconnect()

        # assert
        self.assertTrue(self.command_wrapper.
                        execute_command_with_connection.called_with(self.connection_details,
                                                                    virtual_switch_disconnect_command.disconnect,
                                                                    VmContext.VM_UUID,
                                                                    VmContext.NETWORK_NAME))

    def test_disconnect_all(self):
        # arrange
        virtual_switch_disconnect_command = Mock()
        virtual_switch_disconnect_command.disconnect_all = Mock(return_value=True)
        command_executer_service = CommandExecuterService(Mock(),
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          virtual_switch_disconnect_command,
                                                          Mock())

        CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)

        # act
        command_executer_service.disconnect_all()

        # assert
        self.assertTrue(self.command_wrapper.
                        execute_command_with_connection.called_with(self.connection_details,
                                                                    virtual_switch_disconnect_command.disconnect_all,
                                                                    VmContext.VM_UUID))

    def test_connect_to_first_vnic(self):
        # arrange
        virtual_connect_command = Mock()
        virtual_connect_command.connect_specific_vnic = Mock(return_value=True)
        vc_data_model = Mock()
        vc_data_model.default_dvswitch_path = 'dv path'
        vc_data_model.default_dvswitch_name = 'dv name'
        vc_data_model.default_port_group_path = 'port path'
        command_executer_service = CommandExecuterService(vc_data_model,
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          virtual_connect_command,
                                                          Mock(),
                                                          Mock())

        vm_uuid = CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)
        vlan_id = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_ID)
        vlan_spec_type = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_SPEC_TYPE)


        # act
        command_executer_service.connect_to_first_vnic()

        # assert
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(
            self.connection_details,
            virtual_connect_command.connect_to_first_vnic,
            vm_uuid,
            vlan_id,
            vlan_spec_type,
            vc_data_model.default_dvswitch_path,
            vc_data_model.default_dvswitch_name,
            vc_data_model.default_port_group_path))

    def test_connect_networks(self):
        # arrange
        virtual_connect_command = Mock()
        virtual_connect_command.connect_specific_vnic = Mock(return_value=True)
        vc_data_model = Mock()
        vc_data_model.default_dvswitch_path = 'dv path'
        vc_data_model.default_dvswitch_name = 'dv name'
        vc_data_model.default_port_group_path = 'port path'
        command_executer_service = CommandExecuterService(vc_data_model,
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          virtual_connect_command,
                                                          Mock(),
                                                          Mock())

        CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_ID)
        vm_uuid = CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)
        networks = CommandContextMocker.set_vm_uuid_param(VmContext.NETWORKS)
        vlan_id = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_ID)
        vlan_spec_type = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_SPEC_TYPE)

        # act
        command_executer_service.connect_networks()

        # assert
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(
            self.connection_details,
            virtual_connect_command.connect_networks,
            vm_uuid,
            vlan_id,
            vlan_spec_type,
            networks))

    def test_connect_specific_vnic(self):
        # arrange
        virtual_connect_command = Mock()
        virtual_connect_command.connect_specific_vnic = Mock(return_value=True)
        vc_data_model = Mock()
        vc_data_model.default_dvswitch_path = 'dv path'
        vc_data_model.default_dvswitch_name = 'dv name'
        vc_data_model.default_port_group_path = 'port path'
        command_executer_service = CommandExecuterService(vc_data_model,
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          virtual_connect_command,
                                                          Mock(),
                                                          Mock())

        vm_uuid = CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)
        vnic_name = CommandContextMocker.set_vm_uuid_param(VmContext.VNIC_NAME)
        vlan_id = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_ID)
        vlan_spec_type = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_SPEC_TYPE)

        # act
        command_executer_service.connect_specific_vnic()

        # assert
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(
            self.connection_details,
            virtual_connect_command.connect_specific_vnic,
            vm_uuid,
            vnic_name,
            vlan_id,
            vlan_spec_type,
            vc_data_model.default_dvswitch_path,
            vc_data_model.default_dvswitch_name,
            vc_data_model.default_port_group_path))

    def test_connect_by_mapping(self):
        # arrange
        virtual_connect_command = Mock()
        virtual_connect_command.connect_specific_vnic = Mock(return_value=True)
        vc_data_model = Mock()
        vc_data_model.default_dvswitch_path = 'dv path'
        vc_data_model.default_dvswitch_name = 'dv name'
        vc_data_model.default_port_group_path = 'port path'
        command_executer_service = CommandExecuterService(vc_data_model,
                                                          self.serializer,
                                                          self.quali_helpers,
                                                          self.command_wrapper,
                                                          self.connection_retriever,
                                                          Mock(),
                                                          Mock(),
                                                          Mock(),
                                                          virtual_connect_command,
                                                          Mock(),
                                                          Mock())

        vln_id = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_ID)
        vm_uuid = CommandContextMocker.set_vm_uuid_param(VmContext.VM_UUID)
        vlan_spec_type = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_SPEC_TYPE)
        mapping = CommandContextMocker.set_vm_uuid_param(VmContext.VLAN_MAPPING)

        # act
        command_executer_service.connect_by_mapping()

        # assert
        self.assertTrue(self.command_wrapper.execute_command_with_connection.called_with(
            self.connection_details,
            virtual_connect_command.connect_by_mapping,
            vm_uuid,
            vln_id,
            vlan_spec_type,
            mapping))
