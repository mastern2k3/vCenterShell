from unittest import TestCase
from pyVmomi import vim
from mock import Mock
from vCenterShell.commands.VirtualMachinePortGroupConfigurer import VirtualMachinePortGroupConfigurer


class TestVirtualMachinePortGroupConfigurer(TestCase):
    def setUp(self):
        self.sync_task = Mock()
        self.sync_task.wait_for_task = Mock(return_value=True)

    def test_is_vnic_disconnected(self):
        # arrange
        vnic = Mock()
        vnic.connectable = Mock()
        vnic.connectable.connected = Mock()
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.is_vnic_disconnected(vnic)

        # assert
        self.assertFalse(res)

    def test_is_vnic_attached_to_network_true_port_group(self):
        # arrange
        device = Mock()
        device.backing = Mock()
        device.backing.port = Mock()
        device.backing.port.portgroupKey = 'port'

        network = Mock()
        network.key = device.backing.port.portgroupKey
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.is_vnic_attached_to_network(device, network)

        # assert
        self.assertTrue(res)

    def test_is_vnic_attached_to_network_false_port_group(self):
        # arrange
        device = Mock()
        device.backing = Mock()
        device.backing.port = Mock()
        device.backing.port.portgroupKey = 'port'

        network = Mock()
        network.key = 'false'
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.is_vnic_attached_to_network(device, network)

        # assert
        self.assertFalse(res)

    def test_is_vnic_attached_to_network_false_network(self):
        # arrange
        device = Mock()
        device.backing = Mock()
        device.backing.network = Mock()
        device.backing.network.name = 'name'

        network = Mock()
        network.name = 'false'
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.is_vnic_attached_to_network(device, network)

        # assert
        self.assertFalse(res)

    def test_is_vnic_attached_to_network_true_network(self):
        # arrange
        device = Mock()
        device.backing = Mock()
        device.backing.network = Mock()
        device.backing.network.name = 'name'

        network = Mock()
        network.name = device.backing.network.name
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.is_vnic_attached_to_network(device, network)

        # assert
        self.assertTrue(res)

    def test_is_vnic_attached_to_network_no_backing(self):
        # arrange
        device = Mock(spec=[])

        network = Mock()
        network.name = 'device.backing.network.name'
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.is_vnic_attached_to_network(device, network)

        # assert
        self.assertFalse(res)

    def test_reconfig_vm(self):
        # arrange
        vm = Mock()
        device = Mock()
        task = Mock()
        spec = [Mock(spec=vim.vm.device.VirtualDeviceSpec)]

        vm.ReconfigVM_Task = Mock(return_value=task)
        device.backing = Mock()

        network = Mock()
        network.name = 'device.backing.network.name'
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.reconfig_vm(spec, network)

        # assert
        self.assertTrue(res)

    def test_set_vnic_connectivity_status(self):
        # arrange
        device_spec = Mock()
        device_spec.device = Mock()

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        vmrpgc.set_vnic_connectivity_status(device_spec, True)

        # assert
        self.assertTrue(isinstance(device_spec.device.connectable, vim.vm.device.VirtualDevice.ConnectInfo))
        self.assertTrue(device_spec.device.connectable.connected)
        self.assertTrue(device_spec.device.connectable.startConnected)

    def test_create_vnic_spec(self):
        # arrange
        device = Mock(spec=vim.vm.device.VirtualEthernetCard)
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.create_vnic_spec(device)

        # assert
        self.assertTrue(isinstance(res, vim.vm.device.VirtualDeviceSpec))
        self.assertEqual(res.operation, vim.vm.device.VirtualDeviceSpec.Operation.edit)
        self.assertTrue(res.device, device)

    def test_add_or_update_vnic_network_no_network(self):
        # arrange
        vnic = Mock(spec=vim.vm.device.VirtualEthernetCard)
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.add_or_update_vnic_network(vnic, None)

        # assert
        self.assertIsNone(res)

    def test_add_or_update_vnic_network_no_backing(self):
        # arrange
        network = Mock()
        vnic = Mock(spec=vim.vm.device.VirtualEthernetCard)

        network.key = 'portkey'
        network.config = Mock()
        network.config.distributedVirtualSwitch = Mock()
        network.config.distributedVirtualSwitch.uuid = 'mac address'

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        vmrpgc.add_or_update_vnic_network(vnic, network)

        # assert
        self.assertTrue(isinstance(vnic.backing, vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo))
        self.assertTrue(isinstance(vnic.backing.port, vim.dvs.PortConnection))
        self.assertTrue(vnic.backing.port.portgroupKey, network.key)
        self.assertTrue(vnic.backing.port.switchUuid, network.config.distributedVirtualSwitch.uuid)

    def test_add_or_update_vnic_network_network_set(self):
        # arrange
        network = Mock()
        vnic = Mock(spec=vim.vm.device.VirtualEthernetCard)
        vnic.backing = Mock(spec=vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo)
        vnic.backing.network = network

        network.key = 'portkey'
        network.config = Mock()
        network.config.distributedVirtualSwitch = Mock()
        network.config.distributedVirtualSwitch.uuid = 'mac address'

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        vmrpgc.add_or_update_vnic_network(vnic, network)

        # assert
        self.assertTrue(isinstance(vnic.backing, vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo))
        self.assertTrue(isinstance(vnic.backing.port, vim.dvs.PortConnection))
        self.assertTrue(vnic.backing.port.portgroupKey, network.key)
        self.assertTrue(vnic.backing.port.switchUuid, network.config.distributedVirtualSwitch.uuid)

    def test_get_device_spec(self):
        # arrange
        vnic = Mock(spec=vim.vm.device.VirtualEthernetCard)

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.get_device_spec(vnic, True)

        # assert
        self.assertTrue(isinstance(res, vim.vm.device.VirtualDeviceSpec))
        self.assertTrue(res.device.connectable.connected)
        self.assertTrue(res.device.connectable.startConnected)

    def test_map_vnics(self):
        # arrange
        vnic1 = Mock(spec=vim.vm.device.VirtualEthernetCard)
        vnic1.deviceInfo = Mock()
        vnic1.deviceInfo.label = 'vnic 1'

        vnic2 = Mock(spec=vim.vm.device.VirtualEthernetCard)
        vnic2.deviceInfo = Mock()
        vnic2.deviceInfo.label = 'vnic 2'

        vnic3 = Mock(spec=vim.vm.device.VirtualEthernetCard)
        vnic3.deviceInfo = Mock()
        vnic3.deviceInfo.label = 'vnic 3'

        vm = Mock()
        vm.config = Mock()
        vm.config.hardware = Mock()

        vm.config.hardware.device = [Mock(), vnic1, Mock(), vnic2, vnic3, Mock(), Mock()]

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.map_vnics(vm)

        # assert
        self.assertEqual(res[vnic1.deviceInfo.label], vnic1)
        self.assertEqual(res[vnic2.deviceInfo.label], vnic2)
        self.assertEqual(res[vnic3.deviceInfo.label], vnic3)

    def test_update_vnic_by_mapping_is_none_mapping(self):
        # arrange
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.update_vnic_by_mapping(Mock(), None)

        # assert
        self.assertIsNone(res)

    def test_update_vnic_by_mapping_empty_mapping(self):
        # arrange
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        mapping = dict()
        # act
        res = vmrpgc.update_vnic_by_mapping(Mock(), mapping)

        # assert
        self.assertIsNone(res)

    def test_update_vnic_by_mapping_vm_is_none(self):
        # arrange

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)

        # act
        res = vmrpgc.update_vnic_by_mapping(None, Mock())

        # assert
        self.assertIsNone(res)

    def test_update_vnic_by_mapping(self):
        # arrange
        vm = Mock()

        vnic1 = 'name1'
        network1 = 'network'
        connet1 = 'false'

        vnic2 = 'name2'
        connet2 = 'true'

        vnic3 = 'name3'
        network2 = 'network1'
        connet2 = 'true'

        tup1 = (vnic1, network1, connet1)
        tup2 = (vnic2, network1, connet2)
        tup3 = (vnic3, network2, connet2)

        vm.config.hardware.device = [tup1, tup2, tup3]

        class counter:
            i = 0

        def side_effect(*args, **keys):
            i = counter.i
            counter.i += 1
            return vm.config.hardware.device[i]

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.add_or_update_vnic_network = Mock(return_value=True)
        vmrpgc.get_device_spec = Mock(side_effect=side_effect)
        vmrpgc.reconfig_vm = Mock(return_value=True)

        # act
        res = vmrpgc.update_vnic_by_mapping(vm, vm.config.hardware.device)

        # assert
        self.assertTrue(res)
        self.assertTrue(vmrpgc.reconfig_vm.called_with(vm.config.hardware.device, vm))

    def test_disconnect_network_empty_mapping(self):
        # arrange
        vm = Mock()
        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=None)

        # act
        res = vmrpgc.disconnect_network(vm, None)

        # assert
        self.assertIsNone(res)

    def test_disconnect_network(self):
        # arrange
        vm = Mock()
        network = Mock()
        vnic_name = 'name'
        vnic = Mock()
        vnics_mapping = dict()

        vnics_mapping[vnic_name] = vnic

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnics_mapping)
        vmrpgc.is_vnic_attached_to_network = Mock(return_value=True)
        vmrpgc.is_vnic_disconnected = Mock(return_value=False)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # act
        res = vmrpgc.disconnect_network(vm, network)

        # assert
        self.assertTrue(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertTrue(vmrpgc.is_vnic_attached_to_network.called_with(vnic, network))
        self.assertTrue(vmrpgc.is_vnic_disconnected.called_with(vnic))
        self.assertTrue(vmrpgc.update_vnic_by_mapping.called_with(vm, [(vnic, network, False)]))

    def test_disconnect_network_nothing_to_disconnect(self):
        # arrange
        vm = Mock()
        network = Mock()
        vnic_name = 'name'
        vnic = Mock()
        vnics_mapping = dict()

        vnics_mapping[vnic_name] = vnic

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnics_mapping)
        vmrpgc.is_vnic_attached_to_network = Mock(return_value=False)
        vmrpgc.is_vnic_disconnected = Mock(return_value=True)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # act
        res = vmrpgc.disconnect_network(vm, network)

        # assert
        self.assertIsNone(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertTrue(vmrpgc.is_vnic_attached_to_network.called_with(vnic, network))
        self.assertFalse(vmrpgc.is_vnic_disconnected.called)
        self.assertFalse(vmrpgc.update_vnic_by_mapping.called)

    def test_disconnect_all_port_groups_no_vnics(self):
        # arrange
        vm = Mock()
        vnics_mapping = dict()

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnics_mapping)
        vmrpgc.is_vnic_attached_to_network = Mock(return_value=False)
        vmrpgc.is_vnic_disconnected = Mock(return_value=True)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # act
        res = vmrpgc.disconnect_all_port_groups(vm)

        # assert
        self.assertIsNone(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertFalse(vmrpgc.update_vnic_by_mapping.called)

    def test_disconnect_all_port_groups(self):
        # arrange
        vm = Mock()
        vnic = Mock()
        vnic_name = 'name'
        vnics_mapping = dict()
        vnics_mapping[vnic_name] = vnic

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnics_mapping)
        vmrpgc.is_vnic_attached_to_network = Mock(return_value=False)
        vmrpgc.is_vnic_disconnected = Mock(return_value=True)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # act
        res = vmrpgc.disconnect_all_port_groups(vm)

        # assert
        self.assertTrue(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertTrue(vmrpgc.update_vnic_by_mapping.called_with(vm, [(vnic, None, False)]))

    def test_connect_by_mapping(self):
        # arrange
        vm = Mock()
        network = Mock()
        vnic = Mock()
        vnic_name = 'name'
        vnics_mapping = dict()
        vnics_mapping[vnic_name] = vnic

        connect_mapping = dict()
        connect_mapping[vnic_name] = network

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnics_mapping)
        vmrpgc.is_vnic_attached_to_network = Mock(return_value=False)
        vmrpgc.is_vnic_disconnected = Mock(return_value=True)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # act
        res = vmrpgc.connect_by_mapping(vm, connect_mapping)

        # assert
        self.assertTrue(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertTrue(vmrpgc.update_vnic_by_mapping.called_with(vm, [(vnic, network, True)]))

    def test_connect_by_mapping_vnic_mapping_does_not_contain(self):
        # arrange
        vm = Mock()
        network = Mock()
        vnic = Mock()
        vnic_name = 'name'
        vnics_mapping = dict()
        vnics_mapping[vnic_name] = vnic

        connect_mapping = dict()
        connect_mapping['not found'] = network

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnics_mapping)
        vmrpgc.is_vnic_attached_to_network = Mock(return_value=False)
        vmrpgc.is_vnic_disconnected = Mock(return_value=True)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # act
        res = vmrpgc.connect_by_mapping(vm, connect_mapping)

        # assert
        self.assertIsNone(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertFalse(vmrpgc.update_vnic_by_mapping.called)

    def test_connect_vinc_port_group(self):
        # arrange
        vm = Mock()
        network = Mock()
        vnic_name = 'name'

        called_params = dict()
        called_params[vnic_name] = network

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.connect_by_mapping = Mock(return_value=False)
        # act
        vmrpgc.connect_vinc_port_group(vm, vnic_name, network)

        # assert
        self.assertTrue(vmrpgc.connect_by_mapping.called_with(called_params))

    def test_connect_first_available_vnic(self):
        # arrange
        vm = Mock()
        vnic1 = Mock()
        vnic2 = Mock()
        network = Mock()
        vnic_name1 = 'name 1'
        vnic_name2 = 'name 2'
        vnic_name3 = 'name 3'

        # to check the sorting
        vnic_mapping = dict()
        vnic_mapping[vnic_name2] = vnic2
        vnic_mapping[vnic_name1] = vnic1
        vnic_mapping[vnic_name3] = vnic2

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnic_mapping)
        vmrpgc.is_vnic_disconnected = Mock(return_value=True)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)
        # act
        res = vmrpgc.connect_first_available_vnic(vm, network)

        # assert
        self.assertTrue(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertTrue(vmrpgc.is_vnic_disconnected.called_with(vnic1))
        self.assertTrue(vmrpgc.update_vnic_by_mapping.called_with(vm, [(vnic1, network, True)]))

    def test_connect_first_available_vnic_no_available_vnic(self):
        # arrange
        vm = Mock()
        vnic1 = Mock()
        vnic2 = Mock()
        network = Mock()
        vnic_name1 = 'name 1'
        vnic_name2 = 'name 2'
        vnic_name3 = 'name 3'

        # to check the sorting
        vnic_mapping = dict()
        vnic_mapping[vnic_name2] = vnic2
        vnic_mapping[vnic_name1] = vnic1
        vnic_mapping[vnic_name3] = vnic2

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnic_mapping)
        vmrpgc.is_vnic_disconnected = Mock(return_value=False)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # assert
        self.assertRaises(Exception, vmrpgc.connect_first_available_vnic, vm, network)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertEqual(vmrpgc.is_vnic_disconnected.call_count, 3)
        self.assertFalse(vmrpgc.update_vnic_by_mapping.called)

    def test_connect_networks_no_available_vnic(self):
        # arrange
        vm = Mock()
        vnic1 = Mock()
        vnic2 = Mock()
        network = Mock()
        vnic_name1 = 'name 1'
        vnic_name2 = 'name 2'
        vnic_name3 = 'name 3'

        # to check the sorting
        vnic_mapping = dict()
        vnic_mapping[vnic_name2] = vnic2
        vnic_mapping[vnic_name1] = vnic1
        vnic_mapping[vnic_name3] = vnic2

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnic_mapping)
        vmrpgc.is_vnic_disconnected = Mock(return_value=False)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # assert
        self.assertRaises(Exception, vmrpgc.connect_networks, vm, [network])
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertEqual(vmrpgc.is_vnic_disconnected.call_count, 3)
        self.assertFalse(vmrpgc.update_vnic_by_mapping.called)

    def test_connect_networks(self):
        # arrange
        vm = Mock()
        vnic1 = Mock()
        vnic2 = Mock()
        network = Mock()
        network1 = Mock()
        vnic_name1 = 'name 1'
        vnic_name2 = 'name 2'
        vnic_name3 = 'name 3'

        # to check the sorting
        vnic_mapping = dict()
        vnic_mapping[vnic_name2] = vnic2
        vnic_mapping[vnic_name1] = vnic1
        vnic_mapping[vnic_name3] = vnic2

        vmrpgc = VirtualMachinePortGroupConfigurer(self.sync_task)
        vmrpgc.map_vnics = Mock(return_value=vnic_mapping)
        vmrpgc.is_vnic_disconnected = Mock(return_value=True)
        vmrpgc.update_vnic_by_mapping = Mock(return_value=True)

        # act
        res = vmrpgc.connect_networks(vm, [network, network1])
        # assert
        self.assertTrue(res)
        self.assertTrue(vmrpgc.map_vnics.called_with(vm))
        self.assertEqual(vmrpgc.is_vnic_disconnected.call_count, 2)
        self.assertTrue(vmrpgc.update_vnic_by_mapping.called_with(vm, [(vnic1, network, True),
                                                                       (vnic2, network1, True)]))
