## create the classes of Materials and Processes 
from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, UniqueIdProperty)
from neomodel import db 
import pandas as pd
from termcolor import colored
## define the class for the materials

class Material(StructuredNode):
    """
    A Material is a substance that is used in a process.
    
    It contains the following information: 
        
        - id: unique identifier of the material  
        - name: the name of the material
        - quantity: the quantity of the material
        - unit: the unit which the quantity is measured
        - cost: the price of the material
        - description (optional): a description of the material
    """
    uuid = UniqueIdProperty()
    name = StringProperty()
    quantity = IntegerProperty()
    unit = StringProperty()
    cost = IntegerProperty()
    description = StringProperty()
    associated_materials = RelationshipTo("Material", "USED_WITH")
    associated_processes = RelationshipTo("db.Processes.Process", "USED_IN")
    
    
    ## first need to create all the materials
def material_payload(uuid:str, name:str, quantity:int, unit:str=None, cost:int=None, description:str=None):
    return {"uuid": uuid,
            "name": name+"__",
            "quantity": quantity,
            "unit": unit,
            "cost": cost,
            "description": description}
    
def populate_materials_from_df(df:pd.DataFrame, verbose:bool) -> None:
    """Iterates over a dataframe and add the corresponding data"""
    for row in df.iterrows():
        ## get the row information 
        #process = row[1]['Processes']
        material = row[1]['Material']
        consumption = row[1]['Consumption']
        ## now create the material
        mat_payload = material_payload(uuid=material, name=material, quantity=consumption)
        ## add the material to the database
        #mat = Material.get_or_create(**mat_payload)
        mat = add_material(mat_payload, verbose=verbose)


def add_material(material_dict:dict,verbose:bool) -> bool: 
    """
    Add a new material to the database.
    
    Args:
        material_dict (dict): a dictionary containing the information of the material.
        
    Returns:
        bool: True if the material was added, False otherwise.
    """
    try:
        material = Material.nodes.first_or_none(uuid=material_dict['uuid'])
        if material == None: 
            material = Material(**material_dict).save()
            if verbose:
                print(colored(f"Material: {material_dict['uuid']}-{material_dict['name']} added", "green"))
        else:
            if verbose:
                print(colored(f"Material: {material_dict['uuid']} already exists",'red'))
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