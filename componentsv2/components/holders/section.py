from .nestable import Nestable
from ..base import ComponentV2

from typing import Optional

class Section(Nestable):
    def __init__(self, components: list[ComponentV2], accessory: ComponentV2, id: Optional[int] = None):
        if len(components) < 1 or len(components) > 3:
            raise ValueError("Section can only take 1-3 components and cannot have an empty components table!")
        
        super().__init__(9, id, components)
        self.accessory = accessory

        self.__container_compatible__ = True

    def serialize(self):
        base_dict = super().serialize()
        base_dict["accessory"] = self.accessory.serialize()

        return base_dict