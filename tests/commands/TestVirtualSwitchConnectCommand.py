from unittest import TestCase
from mock import Mock
from vCenterShell.commands.VirtualSwitchConnectCommand import VirtualSwitchConnectCommand


class TestVirtualSwitchConnectCommand(TestCase):
    def test_connect_to_first_vnic(self):
        vln_id = 'id'
        vln_range = 'range'
        port_group_name = 'port name'
        vln_spec = Mock()
        resource_context = Mock()
        session = Mock()
        inventory_path_data = Mock()
        cs_ret_service = Mock()
        virtual_connector = Mock()
        dv_port_name_gen = Mock()
        vlan_spec_factory = Mock()
        vlan_range_parser = Mock()
        resourse_model_parser = Mock()
        helpers = Mock()
        vcenter_resource_details = Mock()
        vcenter_resource_model = Mock()
        resource_context.uuid = 'uuid'
        inventory_path_data.vCenter_resource_name = 'vecenter name'
        vcenter_resource_model.default_dvswitch_path = 'switch path'
        vcenter_resource_model.default_dvswitch_name = 'switch name'
        vcenter_resource_model.default_port_group_path = 'path'

        session.GetResourceDetails = Mock(return_value=vcenter_resource_details)
        helpers.get_api_session = Mock(return_value=session)
        helpers.get_resource_context_details = Mock(return_value=resource_context)
        cs_ret_service.getVCenterInventoryPathAttributeData = Mock(return_value=inventory_path_data)
        resourse_model_parser.convert_to_resource_model = Mock(return_value=vcenter_resource_model)
        vlan_range_parser.parse_vlan_id = Mock(return_value=vln_range)
        dv_port_name_gen.generate_port_group_nae = Mock(return_value=port_group_name)
        vlan_spec_factory.get_vlan_spec = Mock(return_value=vln_spec)
        virtual_connector.connect = Mock(return_value=True)

        command = VirtualSwitchConnectCommand(cs_ret_service, virtual_connector, dv_port_name_gen, vlan_spec_factory,
                                              vlan_range_parser, resourse_model_parser, helpers)

        command.connect_to_first_vnic(vln_id, vln_spec)

        self.assertTrue(helpers.get_resource_context_details.called)
        self.assertTrue(helpers.get_api_session.called)
        self.assertTrue(resourse_model_parser.convert_to_resource_model.called_with(resource_context))
        self.assertTrue(cs_ret_service.getVCenterInventoryPathAttributeData.called_with(resource_context))
        self.assertTrue(session.GetResourceDetails.called_with(inventory_path_data.vCenter_resource_name))
        self.assertTrue(vlan_range_parser.parse_vlan_id.called_with(vln_id))
        self.assertTrue(dv_port_name_gen.generate_port_group_name.called_with(vln_id))
        self.assertTrue(vlan_spec_factory.get_vlan_spec(vln_spec))
        self.assertTrue(virtual_connector.connect.called_with(inventory_path_data.vCenter_resource_name,
                                                              vcenter_resource_model.default_dvswitch_path,
                                                              vcenter_resource_model.default_dvswitch_name,
                                                              port_group_name,
                                                              resource_context.uuid,
                                                              vcenter_resource_model.default_port_group_path,
                                                              vln_range,
                                                              vln_spec))

    def test_connect_specific_vnic(self):
        vnic_name = 'name'
        vln_id = 'id'
        vln_range = 'range'
        port_group_name = 'port name'
        vln_spec = Mock()
        resource_context = Mock()
        session = Mock()
        inventory_path_data = Mock()
        cs_ret_service = Mock()
        virtual_connector = Mock()
        dv_port_name_gen = Mock()
        vlan_spec_factory = Mock()
        vlan_range_parser = Mock()
        resourse_model_parser = Mock()
        helpers = Mock()
        vcenter_resource_details = Mock()
        vcenter_resource_model = Mock()
        resource_context.uuid = 'uuid'
        inventory_path_data.vCenter_resource_name = 'vecenter name'
        vcenter_resource_model.default_dvswitch_path = 'switch path'
        vcenter_resource_model.default_dvswitch_name = 'switch name'
        vcenter_resource_model.default_port_group_path = 'path'

        session.GetResourceDetails = Mock(return_value=vcenter_resource_details)
        helpers.get_api_session = Mock(return_value=session)
        helpers.get_resource_context_details = Mock(return_value=resource_context)
        cs_ret_service.getVCenterInventoryPathAttributeData = Mock(return_value=inventory_path_data)
        resourse_model_parser.convert_to_resource_model = Mock(return_value=vcenter_resource_model)
        vlan_range_parser.parse_vlan_id = Mock(return_value=vln_range)
        dv_port_name_gen.generate_port_group_nae = Mock(return_value=port_group_name)
        vlan_spec_factory.get_vlan_spec = Mock(return_value=vln_spec)
        virtual_connector.connect = Mock(return_value=True)

        command = VirtualSwitchConnectCommand(cs_ret_service, virtual_connector, dv_port_name_gen, vlan_spec_factory,
                                              vlan_range_parser, resourse_model_parser, helpers)

        command.connect_specific_vnic(vln_id, vln_spec, vnic_name)

        self.assertTrue(helpers.get_resource_context_details.called)
        self.assertTrue(helpers.get_api_session.called)
        self.assertTrue(resourse_model_parser.convert_to_resource_model.called_with(resource_context))
        self.assertTrue(cs_ret_service.getVCenterInventoryPathAttributeData.called_with(resource_context))
        self.assertTrue(session.GetResourceDetails.called_with(inventory_path_data.vCenter_resource_name))
        self.assertTrue(vlan_range_parser.parse_vlan_id.called_with(vln_id))
        self.assertTrue(dv_port_name_gen.generate_port_group_name.called_with(vln_id))
        self.assertTrue(vlan_spec_factory.get_vlan_spec(vln_spec))
        self.assertTrue(virtual_connector.connect_specific_vnic.called_with(inventory_path_data.vCenter_resource_name,
                                                                            vcenter_resource_model.default_dvswitch_path,
                                                                            vcenter_resource_model.default_dvswitch_name,
                                                                            port_group_name,
                                                                            resource_context.uuid,
                                                                            vnic_name,
                                                                            vcenter_resource_model.default_port_group_path,
                                                                            vln_range,
                                                                            vln_spec))
