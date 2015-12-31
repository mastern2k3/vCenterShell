from pyVmomi import vim
from pycommon.logger import getLogger

logger = getLogger(__name__)


class VirtualMachinePortGroupConfigurer(object):
    def __init__(self, synchronous_task_waiter):
        self.synchronous_task_waiter = synchronous_task_waiter

    def connect_first_avilaible_vnic(self, vm, network):
        vnic_mapping = self.map_vnics(vm)
        update_mapping = []
        for vnic_name, vnic in vnic_mapping:
            if self.is_vnic_disconnected(vnic):
                return update_mapping.append((vnic, network, True))
                # if self.is_vnic_attached_to_network(vnic, network)
        raise Exception('no available vnic')

    def connect_port_group(self, vm, vnic_name, network):
        """
        this function connect specific vnic to network
        :param vm: virtual machine
        :param vnic_name: the name of the vnic
        :param network: the network to connect to
        """
        mapping = dict()
        mapping[vnic_name] = network
        self.connect_by_mapping(vm, mapping)

    def connect_by_mapping(self, vm, mapping):
        """
        connect connect the vnics to the network by the specification in the mapping
        :param vm: virtual machine
        :param mapping: a dictionary vnic_name to network ({'network 1': <vim.Network>network})
        """
        update_mapping = []
        vnic_mapping = self.map_vnics(vm)
        for vnic_name, network in mapping.items():
            vnic = vnic_mapping[vnic_name]
            if vnic:
                update_mapping.append((vnic, network, True))

        if update_mapping:
            return update_mapping(vm, update_mapping)
        return None

    def disconnect_all_port_groups(self, vm):
        vnics = self.map_vnics(vm)
        update_mapping = []
        for vnic_name, vnic in vnics.items():
            update_mapping.append((vnic, None, False))

        if update_mapping:
            return self.update_vnic_by_mapping(vm, update_mapping)
        return None

    def disconnect_network(self, vm, network):
        vnics = self.map_vnics(vm)
        update_mapping = []
        for vnic_name, vnic in vnics:
            if self.is_vnic_attached_to_network(vnic, network) and \
                    not self.is_vnic_disconnected(vnic):
                update_mapping((vnic, network, False))

        if update_mapping:
            return self.update_vnic_by_mapping(vm, update_mapping)
        return None

    def update_vnic_by_mapping(self, vm, mapping):
        vnics_change = []
        for vnic, network, connect in mapping.items():
            self.add_or_update_vnic_network(vnic, network)
            vnic_spec = self.get_device_spec(vnic, connect)
            vnics_change.append(vnic_spec)

        if vnics_change:
            return self.reconfig_vm(vnics_change, vm)
        return None

    def map_vnics(self, vm):
        """
        maps the vnic of the vm by name
        :param vm: virtual machine
        :return: dictionary: {'vnic_name': vnic}
        """
        mapping = dict()
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                mapping[device.name] = device
        return mapping

    def get_device_spec(self, vnic, set_connected):
        """
        this function creates the device change spec,
        :param vnic: vnic
        :param set_connected: bool, set as connected or not, default: True
        :rtype: device_spec
        """
        nic_spec = self.create_vnic_spec(vnic)
        self.set_vnic_connectivity_status(nic_spec, to_connect=set_connected)
        return nic_spec

    def add_or_update_vnic_network(self, vnic, network):
        """
        attach network to vnic
        :param network: vim.network port group
        :param vnic: vnic
        """
        if network is None:
            return
        dvs_port_connection = vim.dvs.PortConnection()
        dvs_port_connection.portgroupKey = network.key
        dvs_port_connection.switchUuid = network.config.distributedVirtualSwitch.uuid

        # chacking if the vnic is not assigned or assign to a different network
        if not hasattr(vnic, 'backing') or not hasattr(vnic.backing, 'networking'):
            vnic.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()

        vnic.backing.port = dvs_port_connection

    def create_vnic_spec(self, device):
        """
        create device spec for existing device and the mode of edit for the vcenter to update
        :param device:
        :rtype: device spec
        """
        nic_spec = vim.vm.device.VirtualDeviceSpec()
        nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        nic_spec.device = device
        return nic_spec

    def set_vnic_connectivity_status(self, nic_spec, to_connect):
        """
        sets the device spec as connected or disconnected
        :param nic_spec: the specification
        :param to_connect: bool
        """
        nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.connected = to_connect
        nic_spec.device.connectable.startConnected = to_connect

    def reconfig_vm(self, device_change, vm):
        config_spec = vim.vm.ConfigSpec(deviceChange=device_change)
        task = vm.ReconfigVM_Task(config_spec)
        logger.info("Successfully changed network")
        return self.synchronous_task_waiter.wait_for_task(task)

    def is_vnic_attached_to_network(self, device, network):
        if hasattr(device, 'backing'):
            has_port_group_key = hasattr(device.backing, 'port') and hasattr(device.backing.port, 'portgroupKey')
            has_network_name = hasattr(device.backing, 'network') and hasattr(device.backing.network, 'name')
            return (has_port_group_key and device.backing.port.portgroupKey == network.key) or \
                   (has_network_name and device.backing.network.name == network.name)
        return False

    def is_vnic_disconnected(self, vnic):
        is_disconnected = not (hasattr(vnic, 'connectable') and vnic.connectable.connected)
        return is_disconnected
