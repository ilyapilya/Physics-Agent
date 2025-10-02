import sqllite3
from pathlib import Path

class Database:
    def __init__(self):
        self.db_path = Path(__file__) # figure out how to get actual 01-schema.sql path
        self.db_path.parent.mkdir(exist_ok=True)

    def connect(self):
        return sqllite3.connect(self.db_path) 
    
    def init_schema(self):
        with open(Path(__file__).parent / "01-schema.sql", 'r') as f:
            schema = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema)

