

class VirtualSwitchToMachineDisconnectCommand:
    def __init__(self,
                 pyvmomi_service,
                 port_group_configurer):
        self.pyvmomi_service = pyvmomi_service
        self.port_group_configurer = port_group_configurer

    @staticmethod
    def get_network_by_name(vm, network_name):
        for network in vm.network:
            if network_name == network.name:
                return network
        return None

    def disconnect(self, si, vm_uuid, network_name):
        """
        disconnect all of the network adapter of the vm
        :param <str> network_name: the name of the specific network to disconnect
        :param <str> vcenter_name: the name of the vCenter to connect to
        :param <str> vm_uuid: the uuid of the vm
        :return:
        """
        vm = self.pyvmomi_service.find_by_uuid(si, vm_uuid)

        network = self.get_network_by_name(vm, network_name)
        if network is None:
            raise KeyError('network not found ({0})'.format(network_name))

        return self.port_group_configurer.disconnect_network(vm, network)

    def disconnect_all(self, si, vm_uuid):
        """
        disconnect all of the network adapter of the vm
        :param <str> vcenter_name: the name of the vCenter to connect to
        :param <str> vm_uuid: the uuid of the vm
        :return:
        """
        vm = self.pyvmomi_service.find_by_uuid(si, vm_uuid)
        return self.port_group_configurer.disconnect_all_port_groups(vm)
