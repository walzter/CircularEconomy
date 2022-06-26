from warnings import WarningMessage
import neomodel
from dotenv import load_dotenv  # for getting the environment variables
import os

## load the environment variables
load_dotenv()

class DBConnector:
    def __init__(self):
        self._driver = None
        self.uri = os.getenv("base_uri")
        self.user = os.getenv("username")
        self.password = os.getenv("password")
        self.service = os.getenv("service")
        self.url = f"{self.service}://{self.user}:{self.password}@{self.uri}"
        print("Loaded environment variables")

    # connect to the database
    def _connect(self):
        ## start the driver 
        self._driver = neomodel.db
        self._driver.set_connection(self.url)
        print("Connected to the database")

    def _close(self):
        self._driver.driver.close()
        self._driver = None
        print("Terminated connection to the database")

    def _get_session(self):
        """get the session"""
        if self._driver == None: 
            raise RuntimeError("Driver not initialized") from self._driver
        else: 
            return self._driver.driver.session()

    def _clear_database(self):
        """
        Clear the database of all nodes and relationships.
        """
        # run the cypher query to clear the database
        ele = self._driver.db.cypher_quer("MATCH (n) DETACH DELETE n")
        print("Database cleared")
        return ele

    def _get_status(self):
        """Returns the status of the database"""
        if self._driver == None: 
            raise RuntimeError("Driver not initialized") from self._driver
        else: 
            return self._driver.driver.verify_connectivity()
