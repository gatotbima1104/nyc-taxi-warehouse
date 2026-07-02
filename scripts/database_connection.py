from sqlalchemy import create_engine
import psycopg2

class DatabaseConnection():
    def __init__(self, url, host, port, dbname, user, password):
        self.url = url
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        
    def get_engine(self):
        return create_engine(self.url)
    
    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )