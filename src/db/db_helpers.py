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


# Filter a specific material from the database by name and type and return the corresponding node 
def get_material_by_name_and_type(name:str, type:str):
    """
    Get a specific material from the database.
    """
    ele = db.cypher_query("MATCH (n:Material {name: '" + name + "', type: '" + type + "'}) RETURN n")
    return ele


# Get a specific material from the database that matches as input from the database 
def get_material_by_input(name:str):
    """
    Get a specific material from the database.
    """
    ele = db.cypher_query("MATCH (n:Material {input: '" + name + "'}) RETURN n")
    return ele

# Get a specific material from the database that matches as output from the database query
def get_material_by_output(name:str):
    """
    Get a specific material from the database.
    """
    ele = db.cypher_query("MATCH (n:material {output: '" + name + "'}) RETURN n')")
    return ele

# Get materials that are not used by processes
def get_materials_not_used():
    """
    Geting materials that are not used by processes.
    """
    ele = db.cypher_query("MATCH (n:Material) WHERE NOT (n)--(:Process) RETURN n")
    return ele

# Get material names that are not used by processes
def get_material_names_not_used():
    """
    Geting material names that are not used by processes.
    """
    ele = db.cypher_query("MATCH (n:Material) WHERE NOT (n)--(:Process) RETURN n.name")
    return ele

def get_processes_outputs():
    """
    Get the processes outputs that are available to use as input to another process and return the corresponding node.
    """
    ele = db.cypher_query("MATCH (n:Process) WHERE NOT (n)--(:Process) RETURN n")
    return ele

# Get the attributes of a specific process
def get_process_attributes(name:str):
    """
    Get the attributes of a specific process.
    """
    ele = db.cypher_query("MATCH (n:Process {name: '" + name + "'}) RETURN n")
    return ele

# Get the attributes of a specific material
def get_material_attributes(name:str):
    """
    Get the attributes of a specific material.
    """
    ele = db.cypher_query("MATCH (n:Material {name: '" + name + "'}) RETURN n")
    return ele

# Get the count of energy attributes of a specific material
def get_material_energy_attributes_count(name:str):
    """
    Get the count of energy attributes of a specific material.
    """
    ele = db.cypher_query("MATCH (n:Material {name: '" + name + "'}) RETURN count(n.energy)")
    return ele