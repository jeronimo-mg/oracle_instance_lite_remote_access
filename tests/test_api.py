import unittest
from fastapi.testclient import TestClient
import os
import sys
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from api.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('manager.service_manager.ServiceManager.get_all_statuses')
    def test_get_services(self, mock_statuses):
        mock_statuses.return_value = {'weston.service': 'active'}
        response = self.client.get("/services")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'weston.service': 'active'})

    @patch('manager.service_manager.ServiceManager.restart_service')
    def test_restart_service(self, mock_restart):
        mock_restart.return_value = True
        response = self.client.post("/services/weston.service/restart")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})
        mock_restart.assert_called_with('weston.service')

    @patch('manager.db.DatabaseManager.get_logs')
    def test_get_logs(self, mock_logs):
        mock_logs.return_value = [{"id": 1, "service_name": "test", "message": "msg", "timestamp": "now"}]
        response = self.client.get("/logs")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

if __name__ == '__main__':
    unittest.main()
