class VirtualSwitchConnectCommand:
    def __init__(self, pv_service, virtual_switch_to_machine_connector,
                 dv_port_group_name_generator, vlan_spec_factory, vlan_id_range_parser, resourse_model_parser, helpers):
        """
        :type pv_service: object
        :param virtual_switch_to_machine_connector:
        :param dv_port_group_name_generator: DvPortGroupNameGenerator
        :param vlan_spec_factory: VlanSpecFactory
        """
        self.pv_service = pv_service
        self.virtual_switch_to_machine_connector = virtual_switch_to_machine_connector
        self.dv_port_group_name_generator = dv_port_group_name_generator
        self.vlan_spec_factory = vlan_spec_factory  # type: VlanSpecFactory
        self.vlan_id_range_parser = vlan_id_range_parser
        self.resourse_model_parser = resourse_model_parser
        self.helpers = helpers

    def connect_to_first_vnic(self,
                              si,
                              vm_uuid,
                              vlan_id,
                              vlan_spec_type,
                              dv_switch_path,
                              dv_switch_name,
                              port_group_path):

        vm = self.pv_service.find_by_uuid(si, vm_uuid)

        vlan_id_range = self.vlan_id_range_parser.parse_vlan_id(vlan_id)
        dv_port_name = self.dv_port_group_name_generator.generate_port_group_name(vlan_id)
        vlan_spec = self.vlan_spec_factory.get_vlan_spec(vlan_spec_type)

        self.virtual_switch_to_machine_connector.connect(si, vm, dv_switch_path, dv_switch_name,
                                                         dv_port_name, self.vm_uuid, port_group_path, vlan_id_range,
                                                         vlan_spec)

    def connect_specific_vnic(self,
                              si,
                              vm_uuid,
                              vnic_name,
                              vlan_id,
                              vlan_spec_type,
                              dv_switch_path,
                              dv_switch_name,
                              port_group_path):
        vm = self.pv_service.find_by_uuid(si, vm_uuid)

        vlan_id_range = self.vlan_id_range_parser.parse_vlan_id(vlan_id)
        dv_port_name = self.dv_port_group_name_generator.generate_port_group_name(vlan_id)
        vlan_spec = self.vlan_spec_factory.get_vlan_spec(vlan_spec_type)

        self.virtual_switch_to_machine_connector.connect_specific_vnic(si,
                                                                       vm,
                                                                       dv_switch_path,
                                                                       dv_switch_name,
                                                                       dv_port_name,
                                                                       vnic_name,
                                                                       port_group_path,
                                                                       vlan_id_range,
                                                                       vlan_spec)

    def connect_networks(self, si, vm_uuid, vlan_id, vlan_spec_type, networks_mapping):
        vm = self.pv_service.find_by_uuid(si, vm_uuid)
        vlan_spec = self.vlan_spec_factory.get_vlan_spec(vlan_spec_type)

        self.virtual_switch_to_machine_connector.connect_networks(si,
                                                                  vm,
                                                                  vlan_spec,
                                                                  networks_mapping)

    def connect_by_mapping(self, si, vm_uuid, vlan_id, vlan_spec_type, mapping):
        vm = self.pv_service.find_by_uuid(si, vm_uuid)
        vlan_spec = self.vlan_spec_factory.get_vlan_spec(vlan_spec_type)

        self.virtual_switch_to_machine_connector.connect_by_mapping(si,
                                                                    vm,
                                                                    vlan_spec,
                                                                    mapping)
