from datetime import datetime
from utils.helpers import Helper
from scripts.configs import GOLD_SQL_FILES
from scripts.managers import (
    SchemaManager,
    AuditManager
)

class GoldMartBuilder:
    def __init__(self, conn):
        self.conn = conn
        self.schema = SchemaManager(conn)
        self.audit = AuditManager(conn)
        
    def build(self):
        start = datetime.now()
    
        try:
            self.schema.execute_many(GOLD_SQL_FILES)
            
            self.audit.log_pipeline(
                layer="gold",
                process_name="build to gold mart",
                start_time=start,
                end_time=datetime.now(),
                rows_processed=None,
                status="SUCCESS",
                message="[GOLD] gold mart built successfully."
            )
            
            Helper.log(message="Gold Mart built successfully ... ")
            
        except Exception as e:
            self.conn.rollback()
            
            self.audit.log_pipeline(
                layer="gold",
                process_name="build to gold mart",
                start_time=start,
                end_time=datetime.now(),
                rows_processed=0,
                status="FAILED",
                message=f"[ERROR] {str(e)}"
            )
            
            raise