from psycopg2.extensions import connection as PGConnection
from datetime import datetime

class AuditManager():
    def __init__(self, connection: PGConnection):
        self.connection = connection
    
    def log_pipeline(
        self,
        layer: str,
        process_name: str,
        start_time: datetime,
        end_time: datetime,
        rows_processed: int | None,
        status: str,
        message: str | None = None,
    ) -> None:
        query = """
        INSERT INTO audit.logs (
            layer,
            process_name,
            start_time,
            end_time,
            rows_processed,
            status,
            message
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s
        );
        """
        
        values = (
            layer,
            process_name,
            start_time,
            end_time,
            rows_processed,
            status,
            message
        )
        
        with self.connection as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)