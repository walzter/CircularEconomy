from neomodel import db 

def load_env_vars():
    """Loads Environment variables from the .env file """
    from dotenv import load_dotenv ## load the dotenv library
    import os # for getting the environment variables
    load_dotenv()
    base_uri = os.getenv("base_uri")
    username = os.getenv("username")
    password = os.getenv("password")
    print("Loaded environment variables")
    return dict(uri=base_uri, user=username, password=password)

## define function to clear the database of all nodes and relationships 
def clear_db(): 
    """
    Clear the database of all nodes and relationships.
    """
    ele = db.cypher_query("MATCH (n) DETACH DELETE n")
    print("Database cleared")
    return ele


