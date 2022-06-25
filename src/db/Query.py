## class for managing the queries to the database 

class Query:
    
    def __init__(self, database):
        self.db = database 
        self.query = None
    
    def run_query(self):
        return self.db.cypher_query(self.query)
    
    def subgraph_query(self,uuid:str,_type:str):
        ## create the query with the corresponding vars 
        query = f"MATCH (n:{_type} {{uuid: \"{uuid}\"}})-[r]-(m) RETURN r, n, m"
        self.query = query
        
    def material_query(self,uuid:str):
        ## create the query with the corresponding vars 
        query = f"MATCH (n:Material {{uuid: \"{uuid}\"}}) RETURN n"
        self.query = query
    
    def process_query(self,uuid:str):
        ## create the query with the corresponding vars 
        query = f"MATCH (n:Process {{uuid: \"{uuid}\"}}) RETURN n"
        self.query = query