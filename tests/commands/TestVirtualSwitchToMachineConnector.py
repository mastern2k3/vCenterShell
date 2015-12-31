import uuid
from unittest import TestCase

from mock import Mock, MagicMock
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

from pycommon.logging_service import LoggingService
from pycommon.pyVmomiService import pyVmomiService
from tests.testCredentials import TestCredentials
from vCenterShell.commands.VirtualSwitchToMachineConnector import *


class TestVirtualSwitchToMachineConnector(TestCase):
    LoggingService("CRITICAL", "DEBUG", None)

    def test_connect(self):
        # Arrange
        si = Mock()
        network = Mock()
        vm = Mock()

        py_vmomi_service = Mock()
        py_vmomi_service.connect = Mock(return_value=si)
        py_vmomi_service.find_by_uuid = Mock(return_value=vm)

        resource_connection_details_retriever = Mock()
        dv_port_group_creator = MagicMock()
        virtual_machine_port_group_configurer = MagicMock()
        vlan_spec = Mock()
        virtual_switch_to_machine_connector = VirtualSwitchToMachineConnector(py_vmomi_service,
                                                                              resource_connection_details_retriever,
                                                                              dv_port_group_creator,
                                                                              virtual_machine_port_group_configurer)

        virtual_machine_name = 'MachineName'
        vm_uuid = uuid.UUID('{12345678-1234-5678-1234-567812345678}')
        port_group_path = 'QualiSB'
        dv_switch_path = 'QualiSB'
        dv_switch_name = 'dvSwitch'
        dv_port_name = 'dv_port_name'

        # Act
        virtual_switch_to_machine_connector.connect(virtual_machine_name, dv_switch_path, dv_switch_name,
                                                    dv_port_name, vm_uuid,
                                                    port_group_path, 11, vlan_spec)

        # Assert
        self.assertTrue(py_vmomi_service.get_network_by_name_from_vm.called_with(vm, dv_port_name))
        self.assertTrue(virtual_machine_port_group_configurer.connect_port_group.called_with(vm, network))

    def test_connect_specific_vnic(self):
        # Arrange
        si = Mock()
        network = Mock()
        vm = Mock()

        py_vmomi_service = Mock()
        py_vmomi_service.connect = Mock(return_value=si)
        py_vmomi_service.find_by_uuid = Mock(return_value=vm)

        resource_connection_details_retriever = Mock()
        dv_port_group_creator = MagicMock()
        virtual_machine_port_group_configurer = MagicMock()
        vlan_spec = Mock()
        virtual_switch_to_machine_connector = VirtualSwitchToMachineConnector(py_vmomi_service,
                                                                              resource_connection_details_retriever,
                                                                              dv_port_group_creator,
                                                                              virtual_machine_port_group_configurer)

        vcenter_name = 'MachineName'
        vm_uuid = uuid.UUID('{12345678-1234-5678-1234-567812345678}')
        port_group_path = 'QualiSB'
        dv_switch_path = 'QualiSB'
        dv_switch_name = 'dvSwitch'
        dv_port_name = 'dv_port_name'

        # Act
        virtual_switch_to_machine_connector.connect_specific_vnic(vcenter_name,
                                                                  dv_switch_path,
                                                                  dv_switch_name,
                                                                  dv_port_name,
                                                                  vm_uuid,
                                                                  'Network adapter 1',
                                                                  port_group_path,
                                                                  11,
                                                                  vlan_spec)

        # Assert
        self.assertTrue(py_vmomi_service.get_network_by_name_from_vm.called_with(vm, dv_port_name))
        self.assertTrue(virtual_machine_port_group_configurer.connect_port_group.called_with(vm, network))

    def test_connect_specific_vnic(self):
        # Arrange
        si = Mock()
        network = Mock()
        vm = Mock()

        py_vmomi_service = Mock()
        py_vmomi_service.connect = Mock(return_value=si)
        py_vmomi_service.find_by_uuid = Mock(return_value=vm)

        resource_connection_details_retriever = Mock()
        dv_port_group_creator = MagicMock()
        virtual_machine_port_group_configurer = MagicMock()
        vlan_spec = Mock()
        virtual_switch_to_machine_connector = VirtualSwitchToMachineConnector(py_vmomi_service,
                                                                              resource_connection_details_retriever,
                                                                              dv_port_group_creator,
                                                                              virtual_machine_port_group_configurer)

        vm_name = '1'
        vcenter_name = 'vcenter'
        vm_uuid = 'uuid'
        port_group_path = 'QualiSB'
        dv_switch_path = 'QualiSB'
        dv_switch_name = 'dvSwitch'
        vlan_id = 51

        networks = [
            {
                'dv_port_name': 'boris_group22',
                'dv_switch_name': dv_switch_name,
                'dv_switch_path': dv_switch_path,
                'port_group_path': port_group_path,
                'vlan_id': vlan_id
            },
            {
                'dv_port_name': 'boris_group13',
                'dv_switch_name': dv_switch_name,
                'dv_switch_path': dv_switch_path,
                'port_group_path': port_group_path,
                'vlan_id': vlan_id
            }
        ]

        # Act
        virtual_switch_to_machine_connector.connect_networks(vcenter_name,
                                                             vm_uuid,
                                                             vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec(),
                                                             networks)

        # Assert
        self.assertTrue(py_vmomi_service.get_network_by_name_from_vm.called)
        self.assertTrue(virtual_machine_port_group_configurer.connect_port_group.called_with(vm, network))

    def test_connect_by_mapping(self):
        # Arrange
        si = Mock()
        network = Mock()
        vm = Mock()

        py_vmomi_service = Mock()
        py_vmomi_service.connect = Mock(return_value=si)
        py_vmomi_service.find_by_uuid = Mock(return_value=vm)

        resource_connection_details_retriever = Mock()
        dv_port_group_creator = MagicMock()
        virtual_machine_port_group_configurer = MagicMock()
        vlan_spec = Mock()
        virtual_switch_to_machine_connector = VirtualSwitchToMachineConnector(py_vmomi_service,
                                                                              resource_connection_details_retriever,
                                                                              dv_port_group_creator,
                                                                              virtual_machine_port_group_configurer)

        vcenter_name = 'vcenter'
        vm_uuid = 'uuid'
        port_group_path = 'QualiSB'
        dv_switch_path = 'QualiSB'
        dv_switch_name = 'dvSwitch'
        vlan_id = 51

        mapping = {
            'Network adapter 1': {
                'dv_port_name': 'boris_group1',
                'dv_switch_name': dv_switch_name,
                'dv_switch_path': dv_switch_path,
                'port_group_path': port_group_path,
                'vlan_id': vlan_id
            },
            'Network adapter 4': {
                'dv_port_name': 'boris_group10',
                'dv_switch_name': dv_switch_name,
                'dv_switch_path': dv_switch_path,
                'port_group_path': port_group_path,
                'vlan_id': vlan_id
            }
        }

        # Act
        virtual_switch_to_machine_connector.connect_by_mapping(vcenter_name,
                                                               vm_uuid,
                                                               vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec(),
                                                               mapping)

        # Assert
        self.assertTrue(py_vmomi_service.get_network_by_name_from_vm.called)
        self.assertTrue(virtual_machine_port_group_configurer.connect_port_group.called_with(vm, network))

    def get_uuid(self):
        credentials = TestCredentials()
        py_vmomi_service = pyVmomiService(SmartConnect, Disconnect)
        si = py_vmomi_service.connect(credentials.host, credentials.username,
                                      credentials.password,
                                      credentials.port)
        vm_uuid = self.get_vm_uuid(py_vmomi_service, si, 'boris1')
        print vm_uuid

    def get_vm_uuid(self, py_vmomi_service, si, virtual_machine_name):
        vm = py_vmomi_service.get_obj(si.content, [vim.VirtualMachine], virtual_machine_name)
        vm_uuid = vm.config.uuid
        return vm_uuid
