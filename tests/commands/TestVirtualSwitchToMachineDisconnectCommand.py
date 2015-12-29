from unittest import TestCase

from mock import Mock
from pyVmomi import vim

from pycommon.logging_service import LoggingService
from vCenterShell.commands.VirtualSwitchToMachineDisconnectCommand import VirtualSwitchToMachineDisconnectCommand


class TestVirtualSwitchToMachineDisconnectCommand(TestCase):
    LoggingService("CRITICAL", "DEBUG", None)

    def test_delete_all(self):
        # arrange
        uuid = 'uuid'
        vcenter_name = 'vcenter_name'
        si = Mock()
        vm = Mock()

        connection_detail = Mock()
        connection_detail.host = Mock()
        connection_detail.username = Mock()
        connection_detail.password = Mock()
        connection_detail.port = Mock()

        connection_retriever = Mock()
        connection_retriever.connection_details = Mock(return_value=connection_detail)

        pv_service = Mock()
        pv_service.connect = Mock(return_value=si)
        pv_service.find_by_uuid = Mock(return_value=vm)

        virtual_switch_to_machine_connector = \
            VirtualSwitchToMachineDisconnectCommand(pv_service, connection_retriever, Mock(), Mock())
        virtual_switch_to_machine_connector.remove_interfaces_from_vm = Mock(return_value=True)

        # act
        res = virtual_switch_to_machine_connector.disconnect_all(vcenter_name,
                                                                 uuid)
        # assert
        self.assertTrue(connection_retriever.connection_details.called_with(vcenter_name))
        self.assertTrue(pv_service.connect.called_with(connection_detail.host,
                                                       connection_detail.username,
                                                       connection_detail.password,
                                                       connection_detail.port))
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
        self.assertTrue(virtual_switch_to_machine_connector.remove_interfaces_from_vm.called_with(vm))
        self.assertTrue(res)

    def test_delete(self):
        # arrange
        uuid = 'uuid'
        vcenter_name = 'vcenter_name'
        network_name = 'network_name'

        si = Mock()
        vm = Mock()
        network = Mock()

        network.name = network_name
        vm.network = [network]

        connection_detail = Mock()
        connection_detail.host = Mock()
        connection_detail.username = Mock()
        connection_detail.password = Mock()
        connection_detail.port = Mock()

        connection_retriever = Mock()
        connection_retriever.connection_details = Mock(return_value=connection_detail)

        pv_service = Mock()
        pv_service.connect = Mock(return_value=si)
        pv_service.find_by_uuid = Mock(return_value=vm)
        pv_service.get_network_by_name_from_vm = Mock(return_value=network)

        virtual_switch_to_machine_connector = \
            VirtualSwitchToMachineDisconnectCommand(pv_service, connection_retriever, Mock(), Mock())
        virtual_switch_to_machine_connector.remove_interfaces_from_vm = Mock(return_value=True)

        # act
        res = virtual_switch_to_machine_connector.disconnect(vcenter_name,
                                                             uuid,
                                                             network_name)
        # assert
        self.assertTrue(connection_retriever.connection_details.called_with(vcenter_name))
        self.assertTrue(pv_service.connect.called_with(connection_detail.host,
                                                       connection_detail.username,
                                                       connection_detail.password,
                                                       connection_detail.port))
        self.assertTrue(pv_service.find_by_uuid.called_with(si, uuid))
        self.assertTrue(virtual_switch_to_machine_connector.remove_interfaces_from_vm.called)
        self.assertTrue(res)

    def test_get_port_group_key_not_found(self):
        # arrange
        vm = Mock()
        network = Mock()

        network_name = 'will not be found'
        network.name = network_name
        vm.network = [network]

        virtual_switch_to_machine_connector = VirtualSwitchToMachineDisconnectCommand(Mock(), Mock(), Mock(), Mock())

        # act
        res = virtual_switch_to_machine_connector.get_port_group_key(vm, 'Fake name')

        # assert
        self.assertIsNone(res)

