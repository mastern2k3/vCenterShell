from unittest import TestCase
from vCenterShell import bootstrap
from mock import patch, Mock


class MockVCenterDataModelRetriever(object):
    def __init__(self, a, b, c):
        pass

    @staticmethod
    def get_vcenter_data_model(*args):
        return Mock()


class TestBootstrapper(TestCase):
    @patch('common.cloudshell.vc_data_model_retriever.VCenterDataModelRetriever.get_vcenter_data_model',
           MockVCenterDataModelRetriever.get_vcenter_data_model)
    def test_get_command_executer_service(self):
        # Arrange
        bootstrapper = bootstrap.Bootstrapper()

        # Act
        command_executer_service = bootstrapper.get_command_executer_service()

        # Assert
        self.assertIsNotNone(command_executer_service)
