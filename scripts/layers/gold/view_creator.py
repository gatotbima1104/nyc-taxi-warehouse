from scripts.managers import SchemaManager
from scripts.configs import GOLD_VIEW_CREATOR_FILE
from utils.helpers import Helper

class ViewCreator:
    def __init__(self, conn):
        self.conn = conn
        self.schema = SchemaManager(conn)
        
    def create(self):
        self.schema.execute(GOLD_VIEW_CREATOR_FILE)
        Helper.log(message="Views created successfully ... ")