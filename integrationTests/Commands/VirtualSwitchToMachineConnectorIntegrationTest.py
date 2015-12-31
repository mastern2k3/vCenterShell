from unittest import TestCase

from mock import Mock
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

from models.VCenterConnectionDetails import VCenterConnectionDetails
from pycommon.SynchronousTaskWaiter import SynchronousTaskWaiter
from pycommon.logging_service import LoggingService
from pycommon.pyVmomiService import pyVmomiService
from tests.testCredentials import TestCredentials
from vCenterShell.commands.DvPortGroupCreator import DvPortGroupCreator
from vCenterShell.commands.VirtualSwitchToMachineConnector import *


class VirtualSwitchToMachineConnectorIntegrationTest(TestCase):
    LoggingService("CRITICAL", "DEBUG", None)

    def test_connect_first_vnic_integration(self):
        resource_connection_details_retriever = Mock()
        credentials = TestCredentials()
        resource_connection_details_retriever.connection_details = Mock(
                return_value=VCenterConnectionDetails(credentials.host, credentials.username, credentials.password))
        py_vmomi_service = pyVmomiService(SmartConnect, Disconnect)
        synchronous_task_waiter = SynchronousTaskWaiter()

        dv_port_group_creator = DvPortGroupCreator(py_vmomi_service, synchronous_task_waiter)

        virtual_machine_port_group_configurer = VirtualMachinePortGroupConfigurer(synchronous_task_waiter)

        virtual_switch_to_machine_connector = VirtualSwitchToMachineConnector(py_vmomi_service,
                                                                              resource_connection_details_retriever,
                                                                              dv_port_group_creator,
                                                                              virtual_machine_port_group_configurer)

        si = py_vmomi_service.connect(credentials.host, credentials.username,
                                      credentials.password,
                                      credentials.port)

        virtual_machine_path = 'QualiSB/Raz'
        virtual_machine_name = '1'
        vm_uuid = py_vmomi_service.find_vm_by_name(si, virtual_machine_path, virtual_machine_name).config.uuid
        port_group_path = 'QualiSB'
        dv_switch_path = 'QualiSB'
        dv_switch_name = 'dvSwitch'
        dv_port_name = 'boris_group15'

        # Act
        virtual_switch_to_machine_connector.connect(virtual_machine_name,
                                                    dv_switch_path,
                                                    dv_switch_name,
                                                    dv_port_name,
                                                    vm_uuid,
                                                    port_group_path, 51,
                                                    vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec())
