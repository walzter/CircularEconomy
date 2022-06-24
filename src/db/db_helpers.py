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


def get_node_count():
    """
    Get the number of nodes in the database.
    """
    ele = db.cypher_query("MATCH (n) RETURN count(n)")
    return ele[0][0]


def get_processes():
    """
    Get the processes in the database.
    """
    ele = db.cypher_query("MATCH (n:Process) RETURN n")
    return ele

def get_materials():
    """
    Get the materials in the database.
    """
    ele = db.cypher_query("MATCH (n:Material) RETURN n")
    return ele

# get a specific material from the database
def get_material(name:str):
    """
    Get a specific material from the database.
    """
    ele = db.cypher_query("MATCH (n:Material {name: '" + name + "'}) RETURN n")
    return ele

    
# remove a specific material from the database
def remove_material(name:str):
    """
    Remove a specific material from the database.
    """
    ele = db.cypher_query("MATCH (n:Material {name: '" + name + "'}) DETACH DELETE n")
    return ele


