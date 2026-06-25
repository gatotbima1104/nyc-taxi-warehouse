from pathlib import Path
from psycopg2.extensions import connection as PGConnection

class SchemaManager():
    def __init__(self, connection: PGConnection):
        self.connection = connection
        
    @staticmethod
    def read_sql(filepath: Path) -> str:
        with open(filepath, 'r', encoding="utf-8") as f:
            return f.read()
        
    def execute_sql(self, filepath: Path) -> None:
        sql = self.read_sql(filepath)
        with self.connection.cursor() as cur:
            cur.execute(sql)
        
        self.connection.commit()
        print(f'[SCHEMA] Executed {filepath.name}')