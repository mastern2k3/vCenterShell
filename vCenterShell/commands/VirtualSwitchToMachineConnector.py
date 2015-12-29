from vCenterShell.commands.VirtualMachinePortGroupConfigurer import *


class VirtualSwitchToMachineConnector(object):
    def __init__(self, pyvmomi_service, resource_connection_details_retriever, dv_port_group_creator,
                 virtual_machine_port_group_configurer):
        self.pyvmomi_service = pyvmomi_service
        self.resourceConnectionDetailsRetriever = resource_connection_details_retriever
        self.dv_port_group_creator = dv_port_group_creator
        self.virtual_machine_port_group_configurer = virtual_machine_port_group_configurer

    def connect(self, virtual_machine_name, dv_switch_path, dv_switch_name, dv_port_name, virtual_machine_path, vm_uuid,
                port_group_path, vlad_id, vlan_spec):
        connection_details = self.resourceConnectionDetailsRetriever.connection_details(virtual_machine_name)

        si = self.pyvmomi_service.connect(connection_details.host, connection_details.username,
                                          connection_details.password,
                                          connection_details.port)

        logger.debug("virtual machine vmUUID {}".format(vm_uuid))
        vm = self.pyvmomi_service.find_by_uuid(si, vm_uuid)
        network = self.pyvmomi_service.get_network_by_name_from_vm(vm, dv_port_name)

        # checks if the port group is already exist
        if network is None:
            self.dv_port_group_creator.create_dv_port_group(dv_port_name,
                                                            dv_switch_name,
                                                            dv_switch_path,
                                                            si,
                                                            vlan_spec,
                                                            vlad_id)
            # get the network that we created
            network = self.pyvmomi_service.find_network_by_name(si, port_group_path, dv_port_name)

        self.virtual_machine_port_group_configurer.configure_port_group_on_vm(vm, network)
