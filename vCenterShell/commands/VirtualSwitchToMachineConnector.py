from vCenterShell.commands.VirtualMachinePortGroupConfigurer import *


class VirtualSwitchToMachineConnector(object):
    def __init__(self, pyvmomi_service, resource_connection_details_retriever, dv_port_group_creator,
                 virtual_machine_port_group_configurer):
        self.pyvmomi_service = pyvmomi_service
        self.resourceConnectionDetailsRetriever = resource_connection_details_retriever
        self.dv_port_group_creator = dv_port_group_creator
        self.virtual_machine_port_group_configurer = virtual_machine_port_group_configurer

    def connect(self, virtual_machine_name, dv_switch_path, dv_switch_name, dv_port_name, vm_uuid, port_group_path,
                vlad_id, vlan_spec):
        connection_details = self.resourceConnectionDetailsRetriever.connection_details(virtual_machine_name)

        si = self.pyvmomi_service.connect(connection_details.host, connection_details.username,
                                          connection_details.password,
                                          connection_details.port)

        logger.debug("virtual machine vmUUID {}".format(vm_uuid))
        vm = self.pyvmomi_service.find_by_uuid(si, vm_uuid)

        network = self.get_or_create_network(dv_port_name,
                                             dv_switch_name,
                                             dv_switch_path,
                                             port_group_path,
                                             si,
                                             vlad_id,
                                             vlan_spec, vm)

        self.virtual_machine_port_group_configurer.connect_first_available_vnic(vm, network)

    def get_or_create_network(self,
                              dv_port_name,
                              dv_switch_name,
                              dv_switch_path,
                              port_group_path,
                              si,
                              vlad_id,
                              vlan_spec, vm):
        # check if the network is attached to the vm and gets it, the function doesn't goes to the vcenter
        network = self.pyvmomi_service.get_network_by_name_from_vm(vm, dv_port_name)

        # if we didn't found the network on the vm
        if network is None:
            # try to get it from the vcenter
            network = self.pyvmomi_service.find_network_by_name(si, port_group_path, dv_port_name)

        # if we still couldn't get the network ---> create it(can't find it, play god!)
        if network is None:
            self.dv_port_group_creator.create_dv_port_group(dv_port_name,
                                                            dv_switch_name,
                                                            dv_switch_path,
                                                            si,
                                                            vlan_spec,
                                                            vlad_id)
        return network
