class CommandExecuterService(object):
    """ main class that publishes all available commands """

    def __init__(self,
                 vcenter_resource_model,
                 serializer,
                 qualipy_helpers,
                 command_wrapper,
                 connection_retriever,
                 destroy_virtual_machine_command,
                 deploy_from_template_command,
                 virtual_switch_connect_command,
                 virtual_switch_disconnect_command,
                 vm_power_management_command,
                 refresh_ip_command):
        self.vcenter_resource_model = vcenter_resource_model
        self.serializer = serializer
        self.qualipy_helpers = qualipy_helpers
        self.command_wrapper = command_wrapper
        self.connection_retriever = connection_retriever
        self.destroyVirtualMachineCommand = destroy_virtual_machine_command
        self.deployFromTemplateCommand = deploy_from_template_command
        self.virtual_switch_connect_command = virtual_switch_connect_command
        self.virtual_switch_disconnect_command = virtual_switch_disconnect_command
        self.vm_power_management_command = vm_power_management_command
        self.refresh_ip_command = refresh_ip_command

    def connect_to_first_vnic(self):
        # get command parameters from the environment
        vm_uuid = self.qualipy_helpers.get_user_param('VM_UUID')
        vlan_id = self.qualipy_helpers.get_user_param('VLAN_ID')
        vlan_spec_type = self.qualipy_helpers.get_user_param('VLAN_SPEC_TYPE')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.virtual_switch_connect_command.connect_to_first_vnic,
            vm_uuid,
            vlan_id,
            vlan_spec_type,
            self.vcenter_resource_model.default_dvswitch_path,
            self.vcenter_resource_model.default_dvswitch_name,
            self.vcenter_resource_model.default_port_group_path)

    def connect_specific_vnic(self):
        # get command parameters from the environment
        vm_uuid = self.qualipy_helpers.get_user_param('VM_UUID')
        vnic_name = self.qualipy_helpers.get_user_param('VNIC_NAME')
        vlan_id = self.qualipy_helpers.get_user_param('VLAN_ID')
        vlan_spec_type = self.qualipy_helpers.get_user_param('VLAN_SPEC_TYPE')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.virtual_switch_connect_command.connect_specific_vnic,
            vm_uuid,
            vnic_name,
            vlan_id,
            vlan_spec_type,
            self.vcenter_resource_model.default_dvswitch_path,
            self.vcenter_resource_model.default_dvswitch_name,
            self.vcenter_resource_model.default_port_group_path)

    def connect_networks(self):
        # get command parameters from the environment
        vm_uuid = self.qualipy_helpers.get_user_param('VM_UUID')
        vlan_id = self.qualipy_helpers.get_user_param('VLAN_ID')
        vlan_spec_type = self.qualipy_helpers.get_user_param('VLAN_SPEC_TYPE')
        networks = self.qualipy_helpers.get_user_param('NETWORKS')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.virtual_switch_connect_command.connect_networks,
            vm_uuid,
            vlan_id,
            vlan_spec_type,
            networks)

    def connect_by_mapping(self):
        # get command parameters from the environment
        vm_uuid = self.qualipy_helpers.get_user_param('VM_UUID')
        vlan_id = self.qualipy_helpers.get_user_param('VLAN_ID')
        vlan_spec_type = self.qualipy_helpers.get_user_param('VLAN_SPEC_TYPE')
        mapping = self.qualipy_helpers.get_user_param('VLAN_MAPPING')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.virtual_switch_connect_command.connect_by_mapping,
            vm_uuid,
            vlan_id,
            vlan_spec_type,
            mapping)

    def disconnect_all(self):
        # get command parameters from the environment
        virtual_machine_id = self.qualipy_helpers.get_user_param('VM_UUID')
        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.virtual_switch_disconnect_command.disconnect_all,
            virtual_machine_id)

    def disconnect(self):
        # get command parameters from the environment
        virtual_machine_id = self.qualipy_helpers.get_user_param('VM_UUID')
        network_name = self.qualipy_helpers.get_user_param('NETWORK_NAME')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.virtual_switch_disconnect_command.disconnect,
            virtual_machine_id,
            network_name)

    def destroy(self):
        # get command parameters from the environment
        uuid = self.qualipy_helpers.get_user_param('uuid')
        resource = self.qualipy_helpers.get_resource_context_details()

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.destroyVirtualMachineCommand.destroy,
            uuid,
            resource.fullname)

    def deploy_from_template(self):
        # get command parameters from the environment
        deployment_params = self.qualipy_helpers.get_user_param('DEPLOY_DATA')
        data = self.serializer.decode(deployment_params)

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        result = self.command_wrapper.execute_command_with_connection(
            connection_details,
            self.deployFromTemplateCommand.execute_deploy_from_template,
            data)
        print self.serializer.encode(result)

    def power_off(self):
        # get command parameters from the environment
        vm_uuid = self.qualipy_helpers.get_user_param('VM_UUID')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(connection_details,
                                                             self.vm_power_management_command.power_off,
                                                             vm_uuid)

    def power_on(self):
        # get command parameters from the environment
        vm_uuid = self.qualipy_helpers.get_user_param('VM_UUID')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.command_wrapper.execute_command_with_connection(connection_details,
                                                             self.vm_power_management_command.power_on,
                                                             vm_uuid)

    def refresh_ip(self):
        # get command parameters from the environment
        vm_uuid = self.qualipy_helpers.get_user_param('VM_UUID')
        resource_name = self.qualipy_helpers.get_user_param('RESOURCE_NAME')

        # prepare for execute command
        connection_details = self.connection_retriever.connection_details()

        # execute command
        self.execute_command_with_connection(connection_details,
                                             self.refresh_ip_command.refresh_ip,
                                             vm_uuid,
                                             resource_name)
