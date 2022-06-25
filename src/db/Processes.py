from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, UniqueIdProperty,RelationshipFrom)
from db.Materials import Material
import pandas as pd 
from termcolor import colored
## define the class for the processes
class Process(StructuredNode):
    """
    A Process is a process that is used to produce a material.
    
    It contains the following information: 
        
        - uuid: unique identifier of the process  
        - name: the name of the process
        - materials used in the process (input/output): a list of materials
        - output of the process: the material(s) produced
        - description (optional): a description of the process
    """
    uuid = UniqueIdProperty()
    name = StringProperty()
    output_material = RelationshipTo("db.Materials.Material", "OUTPUT_MATERIAL")
    input_material = RelationshipFrom("db.Materials.Material", "INPUT_MATERIAL")
    description = StringProperty()
    total_input_cost = IntegerProperty()
    total_output_cost = IntegerProperty()
    
## create the process payload 
def process_payload(uuid:str, name:str, output_materials:str=None, input_materials:str=None, description:str=None, total_input_cost:int=None, total_output_cost:int=None):
    return {"uuid": uuid,
            "name": name,
            "output_materials": output_materials,
            "input_materials": input_materials,
            "description": description,
            "total_input_cost": total_input_cost,
            "total_output_cost": total_output_cost}
    
    
def populate_process_from_df(df:pd.DataFrame,verbose:bool) -> None:
    for rows in df.iterrows():
    ## get the row 
        row = rows[1]
        process = row['Processes']
        material = row['Material']
        material_obj = Material.nodes.filter(uuid=material)[0]
        process_name = row['Processes']+"__XX" ## add a random string to the process name to avoid duplicates
        consumption = row['Consumption']
        is_input = consumption < 0
        ## create the process
        if is_input: 
            input_material = material_obj
            data_payload = process_payload(uuid=process,
                                    name=process_name,
                                    input_materials=material)
            ## add to database
            proc,_ = add_process(data_payload, verbose=verbose)
            ## add the connection 
            proc.input_material.connect(input_material).save()
        else: 
            output_material = material_obj
            data_payload = process_payload(uuid=process,
                                    name=process_name,
                                    output_materials=material)
            ## add to database
            proc,_ = add_process(data_payload, verbose=verbose)
            ## add the connection 
            proc.output_material.connect(output_material).save()
            
            
def add_process(process_dict:dict, verbose:bool):
    """
    Add a process to the database
    """
    try: 
        process = Process.nodes.first_or_none(uuid=process_dict['uuid'])
        if process == None:
            process = Process(**process_dict).save()
            if verbose:
                print(colored(f"Process {process.uuid} added", 'green'))
        else:
            if verbose:
                print(colored(f"Process {process.uuid} already exists", 'red'))
        return process, True
    except Exception as e:
        print(e)
        return process, False
