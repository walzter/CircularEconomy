from neomodel import db 
from db.Materials import Material 

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


def add_material(material_dict:dict) -> bool: 
    """
    Add a new material to the database.
    
    Args:
        material_dict (dict): a dictionary containing the information of the material.
        
    Returns:
        bool: True if the material was added, False otherwise.
    """
    try:
        material = Material(**material_dict).save()
        print(f"Material: {material_dict['uuid']}-{material_dict['name']} added")
        return material, True
    except Exception as e:
        print(e)
        return False

def remove_material(material_id:str) -> bool: 
    """
    Remove a material from the database.
    
    Args:
        material_id (str): the id of the material to be removed.
        
    Returns:
        bool: True if the material was removed, False otherwise.
    """
    try:
        Material.nodes.get(uuid=material_id).delete()
        print(f"Material: {material_id} deleted")
        return True
    except Exception as e:
        print(e)
        return False

## define functions to update the Materials 
@db.transaction
def update_material_name(material_id:str, new_name:str) -> bool: 
    """
    Update the name of a material.
    
    Args:
        material_id (str): the id of the material to be updated.
        new_name (str): the new name of the material.
        
    Returns:
        bool: True if the material was updated, False otherwise.
    """
    try:
        material = Material.nodes.filter(uuid=material_id)[0]
        ## replace the name
        material.name = new_name
        ## save it 
        material.save()
        print(f"Updated Material: {material_id} with new name: {new_name}")
        return True
    except Exception as e:
        print(e)
        return False
    
def update_material_quantity(material_id:str, new_quantity:int) -> bool:
    """
    Update the quantity of a material.
    
    Args:
        material_id (str): the id of the material to be updated.
        new_quantity (int): the new quantity of the material.
        
    Returns:
        bool: True if the material was updated, False otherwise.
    """
    try:
        material = Material.nodes.filter(uuid=material_id)[0]
        ## replace the quantity
        material.quantity = new_quantity
        ## save it 
        material.save()
        print(f"Updated Material: {material_id} with new quantity: {new_quantity}")
        return True
    except Exception as e:
        print(e)
        return False

def add_material_relationship(material1:str, material2:str) -> bool:
    """Adds a relationship between two materials"""
    try:
        material1.associated_materials.connect(material2)
        print(f"Added relationship between {material1.uuid} and {material2.uuid}")
        return True
    except Exception as e: 
        print(e)
        return False

## define function to clear the database of all nodes and relationships 
def clear_db(): 
    """
    Clear the database of all nodes and relationships.
    """
    ele = db.cypher_query("MATCH (n) DETACH DELETE n")
    print("Database cleared")
    return ele


