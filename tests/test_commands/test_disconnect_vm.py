from unittest import TestCase
from mock import Mock
from vCenterShell.commands.disconnect_dvswitch import VirtualSwitchToMachineDisconnectCommand


class TestVirtualSwitchToMachineDisconnectCommand(TestCase):
    def test_disconnect_all(self):
        # arrange
        uuid = 'uuid'
        vcenter_name = 'vcenter_name'
        si = Mock()
        vm = Mock()

        pv_service = Mock()
        pv_service.find_by_uuid = Mock(return_value=vm)
        port_group_configurer = Mock()
        port_group_configurer.disconnect_all_port_groups = Mock(return_value=True)
        virtual_switch_to_machine_connector = \
            VirtualSwitchToMachineDisconnectCommand(pv_service, port_group_configurer)

        # act
        res = virtual_switch_to_machine_connector.disconnect_all(vcenter_name,
                                                                 uuid)
        # assert
        self.assertTrue(res)
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
        self.assertTrue(port_group_configurer.disconnect_all_port_groups.called_with(vm))

    def test_disconnect(self):
        # arrange
        uuid = 'uuid'
        network_name = 'network_name'
        si = Mock()
        vm = Mock()
        network = Mock()
        pv_service = Mock()
        port_config = Mock()

        port_config.disconnect_network = Mock(return_value=True)
        network.name = network_name
        vm.network = [network]
        pv_service.find_by_uuid = Mock(return_value=vm)
        pv_service.get_network_by_name_from_vm = Mock(return_value=network)

        virtual_switch_to_machine_connector = \
            VirtualSwitchToMachineDisconnectCommand(pv_service, port_config.disconnect_network)
        # act
        res = virtual_switch_to_machine_connector.disconnect(si,
                                                             uuid,
                                                             network_name)
        # assert
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
        self.assertTrue(port_config.disconnect_network(vm, network))
        self.assertTrue(res)

    def test_disconnect_network_not_found(self):
        # arrange
        uuid = 'uuid'
        not_found = 'aaa'
        network_name = 'network_name'
        si = Mock()
        vm = Mock()
        network = Mock()
        pv_service = Mock()
        port_config = Mock()

        port_config.disconnect_network = Mock(return_value=True)
        network.name = network_name
        vm.network = [network]
        pv_service.find_by_uuid = Mock(return_value=vm)
        pv_service.get_network_by_name_from_vm = Mock(return_value=network)

        virtual_switch_to_machine_connector = \
            VirtualSwitchToMachineDisconnectCommand(pv_service, port_config.disconnect_network)
        # act
        self.assertRaises(Exception,
                          virtual_switch_to_machine_connector.disconnect,
                          si,
                          uuid,
                          not_found)
        # assert
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
        self.assertTrue(port_config.disconnect_network(vm, not_found))
