import unittest
import os
import sys
import sqlite3

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from manager.db import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_litemode.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.db = DatabaseManager(self.db_path)
        self.db.init_db()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_db(self):
        # Verify tables exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='services'")
        self.assertIsNotNone(cursor.fetchone())
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
        self.assertIsNotNone(cursor.fetchone())
        conn.close()

    def test_upsert_service(self):
        self.db.upsert_service('weston.service', 'active')
        service = self.db.get_service('weston.service')
        self.assertEqual(service['name'], 'weston.service')
        self.assertEqual(service['status'], 'active')

    def test_add_log(self):
        self.db.add_log('weston.service', 'Started successfully')
        logs = self.db.get_logs(limit=1)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['service_name'], 'weston.service')
        self.assertEqual(logs[0]['message'], 'Started successfully')

if __name__ == '__main__':
    unittest.main()
