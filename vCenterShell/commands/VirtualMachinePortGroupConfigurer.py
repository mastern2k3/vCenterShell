from pyVmomi import vim
from pycommon.logger import getLogger

from pycommon.pyVmomiService import *

logger = getLogger(__name__)


class VirtualMachinePortGroupConfigurer(object):
    def __init__(self, synchronous_task_waiter):
        self.synchronous_task_waiter = synchronous_task_waiter

    def connect_port_group(self, vm, network):
        """
        configures on the first network adapter on vm the connectivity to that network
        :param vm: vim.VirtualMachine
        :param network: vim.Network
        """
        device_change = []
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard) and \
                    self.device_is_attached_to_network(device, network):
                nic_spec = self.get_nic_spec(device)
                nic_spec.device.wakeOnLanEnabled = True

                # set connectivity
                self.set_nic_connectivity_status(nic_spec, is_connected=True)

                device_change.append(nic_spec)
                # break

        # if none found, create new one adapter
        if len(device_change) == 0:
            device = vim.vm.device.VirtualVmxnet()
            nic_spec = self.get_nic_spec(device)
            nic_spec.device.wakeOnLanEnabled = True
            # connect to port group
            dvs_port_connection = vim.dvs.PortConnection()
            dvs_port_connection.portgroupKey = network.key
            dvs_port_connection.switchUuid = network.config.distributedVirtualSwitch.uuid
            nic_spec.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            nic_spec.device.backing.port = dvs_port_connection
            self.set_nic_connectivity_status(nic_spec, is_connected=True)
            device_change.append(nic_spec)

        return self.reconfig_vm(device_change, vm)

    def disconnect_port_group(self, vm, network):
        self.disconnect_port_groups_by_filter(vm,
                                              lambda device: self.device_is_attached_to_network(device, network))

    def disconnect_all_port_groups(self, vm):
        self.disconnect_port_groups_by_filter(vm)

    def disconnect_port_groups_by_filter(self, vm, filter_action=None):
        device_change = []
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                if filter_action is None or filter_action(device):
                    nic_spec = self.get_nic_spec(device)
                    self.set_nic_connectivity_status(nic_spec, is_connected=False)
                    device_change.append(nic_spec)

        if len(device_change) > 0:
            return self.reconfig_vm(device_change, vm)
        return None

    def set_nic_connectivity_status(self, nic_spec, is_connected):
        nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.connected = is_connected
        nic_spec.device.connectable.startConnected = is_connected

    def reconfig_vm(self, device_change, vm):
        config_spec = vim.vm.ConfigSpec(deviceChange=device_change)
        task = vm.ReconfigVM_Task(config_spec)
        logger.info("Successfully changed network")
        return self.synchronous_task_waiter.wait_for_task(task)

    def get_nic_spec(self, device):
        nic_spec = vim.vm.device.VirtualDeviceSpec()
        nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        nic_spec.device = device
        return nic_spec

    def device_is_attached_to_network(self, device, network):
        has_port_group_key = hasattr(device, 'port') and hasattr(device.port, 'portgroupKey')
        has_network_name = hasattr(device, 'network') and hasattr(device.network, 'name')
        return (has_port_group_key and device.port.portgroupKey == network.key) or \
               (has_network_name and device.network.name == network.name)
