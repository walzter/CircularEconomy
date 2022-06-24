from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, UniqueIdProperty,RelationshipFrom)
from db.Materials import Material
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
    