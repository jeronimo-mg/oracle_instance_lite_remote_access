import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from manager.service_manager import ServiceManager

class TestServiceManager(unittest.TestCase):
    def setUp(self):
        self.manager = ServiceManager(services=['weston.service', 'novnc.service'])

    @patch('subprocess.run')
    def test_check_service_status_active(self, mock_run):
        # Mock active service
        mock_run.return_value = MagicMock(returncode=0)
        status = self.manager.check_status('weston.service')
        self.assertTrue(status)
        mock_run.assert_called_with(['systemctl', 'is-active', 'weston.service'], capture_output=True, text=True)

    @patch('subprocess.run')
    def test_check_service_status_inactive(self, mock_run):
        # Mock inactive service
        mock_run.return_value = MagicMock(returncode=3) # inactive (dead) usually returns non-zero
        status = self.manager.check_status('novnc.service')
        self.assertFalse(status)

    @patch('subprocess.run')
    def test_restart_service(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        success = self.manager.restart_service('weston.service')
        self.assertTrue(success)
        # Check if sudo was used as it's a system service
        mock_run.assert_called_with(['sudo', 'systemctl', 'restart', 'weston.service'], capture_output=True, text=True)

    @patch('subprocess.run')
    def test_check_status_exception(self, mock_run):
        mock_run.side_effect = Exception("System error")
        status = self.manager.check_status('any.service')
        self.assertFalse(status)

    @patch('subprocess.run')
    def test_restart_service_exception(self, mock_run):
        mock_run.side_effect = Exception("System error")
        success = self.manager.restart_service('any.service')
        self.assertFalse(success)

    def test_get_all_statuses(self):
        with patch.object(self.manager, 'check_status') as mock_check:
            mock_check.side_effect = [True, False]
            statuses = self.manager.get_all_statuses()
            self.assertEqual(statuses, {
                'weston.service': 'active',
                'novnc.service': 'inactive'
            })

if __name__ == '__main__':
    unittest.main()
