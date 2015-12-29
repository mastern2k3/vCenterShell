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
                    self.device_is_attached_to_network_or_disconnected(device, network):
                nic_spec = self.get_nic_spec(device)
                nic_spec.device.wakeOnLanEnabled = True

                # set connectivity
                self.set_nic_connectivity_status(nic_spec, is_connected=True)

                device_change.append(nic_spec)
                break

        if device_change:
            return self.reconfig_vm(device_change, vm)
        else:
            raise Exception('there is no vnic available')

    def disconnect_port_group(self, vm, network):
        return self.disconnect_port_groups_by_filter(vm,
                                                     lambda device: self.device_is_attached_to_network_or_disconnected(
                                                         device, network))

    def disconnect_all_port_groups(self, vm):
        return self.disconnect_port_groups_by_filter(vm)

    def disconnect_port_groups_by_filter(self, vm, filter_action=None):
        disconnected_network = []
        device_change = []
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                if filter_action is None or filter_action(device):
                    disconnected_network.append(device.backing)
                    nic_spec = self.get_nic_spec(device)
                    self.set_nic_connectivity_status(nic_spec, is_connected=False)
                    device_change.append(nic_spec)

        if device_change:
            self.reconfig_vm(device_change, vm)

        return disconnected_network

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

    def device_is_attached_to_network_or_disconnected(self, device, network):
        if hasattr(device, 'backing'):
            has_port_group_key = hasattr(device.backing, 'port') and hasattr(device.backing.port, 'portgroupKey')
            has_network_name = hasattr(device.backing, 'network') and hasattr(device.backing.network, 'name')
            is_disconnected = not (hasattr(device, 'connectable') and device.connectable.connected)
            return is_disconnected or \
                   (has_port_group_key and device.backing.port.portgroupKey == network.key) or \
                   (has_network_name and device.backing.network.name == network.name)
        return False

    def map_vnics_networks(self, vm):
        vnics_to_network_mapping = dict()
        network_mapping = dict()
        for network in vm.network:
            # checks if has key att otherwise it takes the name of the network
            # todo: check if name of the network is known network, that matches our standards or default,
            # todo: otherwise return mark the vnic that is connected to it as unassigned
            key = network.key if hasattr(network, 'key') else network.name

            network_mapping[key] = network

        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                # get the correct network
                if hasattr(device.backing, 'port') and hasattr(device.backing.port, 'portgroupKey'):
                    network = network_mapping[device.backing.port.portgroupKey]
                elif hasattr(device.backing, 'network') and hasattr(device.backing.network, 'name'):
                    network = network_mapping[device.backing.network.name]
                else:
                    network = None

                # check the status of vnic regars to the network
                if network:
                    is_connected = self.device_is_attached_to_network_or_disconnected(device, network)
                    vnics_to_network_mapping[network.name] = {'device': device,
                                                              'is_connected': is_connected}
                else:
                    vnics_to_network_mapping['unassigned'](device)

        return vnics_to_network_mapping
