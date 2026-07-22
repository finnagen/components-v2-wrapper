from ..base import ComponentV2
from typing import Optional

class Nestable(ComponentV2): ## a 'Nestable' base class is able to nest other components inside of itself. Action rows are intentionally left out of this class, as it exclusive for ComponentsV2.
    def __init__(self, type: int, id: Optional[int] = None, components: list[ComponentV2] = None):
        super().__init__(type, id)

        if components is None:
            components = []
            
        self.components = components

    def to_component_list(self):
        components = []

        for component in self.components:
            components.append(component.serialize())

        return components
    
    def serialize(self):
        base_dict = super().serialize()
        base_dict["components"] = self.to_component_list()
        
        return base_dict