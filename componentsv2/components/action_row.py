from .base import ComponentV2
from typing import Optional

class ActionRow(ComponentV2):
    types_to_max = {
        2: 5,

        3: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 1,
    }

    def __init__(self, id: Optional[int] = None):
        super().__init__(1, id)

        self.component_type: Optional[int] = None
        self.components: list[ComponentV2] = []

        self.__container_compatible__ = True
    
    def serialize(self) -> dict:
        base_dict: dict = super(ActionRow, self).serialize()
        component_array = []

        for component in self.components:
            component_array.append(component.serialize())

        base_dict["components"] = component_array
        return base_dict
    
    def append_component(self, component: ComponentV2):
        if self.component_type != None and component.type != self.component_type:
            raise TypeError("Cannot assign multiple different types to one action row.")
        
        max = self.types_to_max[component.type]
        if max == None:
            raise TypeError(f"Component type {component.type} not accepted in an action row!")

        if len(self.components) >= max:
            raise ValueError(f"Cannot add more components to this action row! Max: {max}")
        
        self.components.append(component)