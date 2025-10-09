import sqlite3
from pathlib import Path

class Database:
    def __init__(self):
        self.db_path = Path(__file__).parent / "physics.db"
        self.schema_path = Path(__file__).parent / "01-schema.sql"
        self.db_path.parent.mkdir(exist_ok=True)
        
    def get_connection(self):
        return sqlite3.connect(str(self.db_path))
    
    def init_db(self):
        """Initialize database with schema"""
        with open(self.schema_path, 'r') as f:
            schema = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema)