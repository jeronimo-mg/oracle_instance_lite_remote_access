import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_path="litemode.db"):
        self.db_path = db_path

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes the database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS services (
                    name TEXT PRIMARY KEY,
                    status TEXT,
                    last_check DATETIME,
                    enabled INTEGER DEFAULT 1
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    service_name TEXT,
                    message TEXT
                )
            """)
            conn.commit()

    def upsert_service(self, name, status):
        """Inserts or updates service status."""
        now = datetime.datetime.now()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO services (name, status, last_check)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    status=excluded.status,
                    last_check=excluded.last_check
            """, (name, status, now))
            conn.commit()

    def get_service(self, name):
        """Returns service info as a dict."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM services WHERE name=?", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def add_log(self, service_name, message):
        """Adds a log entry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs (service_name, message)
                VALUES (?, ?)
            """, (service_name, message))
            conn.commit()

    def get_logs(self, limit=50):
        """Returns the latest log entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]
