# -*- coding: utf-8 -*-
"""
@see https://waffle.io/QualiSystems/vCenterShell/cards/5666b2aa0c076d2300052216 for initial info

@see https://www.vmware.com/support/developer/vc-sdk/visdk41pubs/ApiReference/vim.DistributedVirtualSwitch.html
"""

from pyVmomi import vim
from pycommon.pyVmomiService import *
from pycommon.logger import getLogger

_logger = getLogger("vCenterShell")


class VirtualSwitchToMachineDisconnectCommand:
    def __init__(self,
                 pyvmomi_service,
                 connection_retriever,
                 port_group_configurer):
        self.pyvmomi_service = pyvmomi_service
        self.connection_retriever = connection_retriever
        self.port_group_configurer = port_group_configurer

    def get_network_by_name(self, vm, network_name):
        for network in vm.network:
            if network_name == network.name:
                return network
        return None

    def disconnect(self, vcenter_name, vm_uuid, network_name):
        """
        disconnect all of the network adapter of the vm
        :param <str> network_name: the name of the specific network to disconnect
        :param <str> vcenter_name: the name of the vCenter to connect to
        :param <str> vm_uuid: the uuid of the vm
        :return:
        """
        connection_details = self.connection_retriever.connection_details(vcenter_name)

        si = self.pyvmomi_service.connect(connection_details.host, connection_details.username,
                                          connection_details.password,
                                          connection_details.port)
        _logger.debug("Revoking ALL Interfaces from VM '{}'".format(vm_uuid))

        vm = self.pyvmomi_service.find_by_uuid(si, vm_uuid)

        network = self.get_network_by_name(vm, network_name)
        if network is None:
            raise KeyError('network not found ({0})'.format(network_name))

        return self.port_group_configurer.disconnect_network(vm, network)

    def disconnect_all(self, vcenter_name, vm_uuid):
        """
        disconnect all of the network adapter of the vm
        :param <str> vcenter_name: the name of the vCenter to connect to
        :param <str> vm_uuid: the uuid of the vm
        :return:
        """
        connection_details = self.connection_retriever.connection_details(vcenter_name)

        si = self.pyvmomi_service.connect(connection_details.host, connection_details.username,
                                          connection_details.password,
                                          connection_details.port)
        _logger.debug("Revoking ALL Interfaces from VM '{}'".format(vm_uuid))

        vm = self.pyvmomi_service.find_by_uuid(si, vm_uuid)
        return self.port_group_configurer.disconnect_all_port_groups(vm)
