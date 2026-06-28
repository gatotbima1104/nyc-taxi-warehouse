from pathlib import Path
from psycopg2.extensions import connection as PGConnection

class SchemaManager():
    def __init__(self, connection: PGConnection):
        self.connection = connection
        
    @staticmethod
    def read(filepath: Path) -> str:
        with open(filepath, 'r', encoding="utf-8") as f:
            return f.read()
        
    def execute(self, filepath: Path) -> None:
        sql = self.read(filepath)
        with self.connection.cursor() as cur:
            cur.execute(sql)
        
        self.connection.commit()
        print(f'[SCHEMA] Executed {filepath.name}')
        
    def execute_many(self, filepath: list[Path]) -> None:
        with self.connection.cursor() as cur:
            for filepath in filepath:
                sql = self.read(filepath)
                cur.execute(sql)
                print(f'[SQL] Executed {filepath.name}')
        
        self.connection.commit()

    def fetch(self, sql: str):
        with self.connection.cursor() as cur:
            cur.execute(sql)
            return cur.fetchone()[0]