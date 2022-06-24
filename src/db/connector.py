from neomodel import db 

class DBConnector:
    
    def __init__(self, uri, user, password):
        self.uri = uri 
        self.user = user 
        self.password = password 
        self.url = self._make_connection_url()
    ## create the connection url 
    def _make_connection_url(self):
        """Returns the connection URL and the driver."""
        return f"neo4j://{self.user}:{self.password}@{self.uri}"
    
    ## connect to the database 
    def _connect(self):
        db.set_connection(self.url)
        print("Connected to the database")
        
    def _close(self):
        db.driver.close()
        print("Terminated connection to the database")
    