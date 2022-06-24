## create the classes of Materials and Processes 
from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, UniqueIdProperty)

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
    
    