from .base import ComponentV2
from typing import Optional

class TextDisplay(ComponentV2):
    def __init__(self, content: str, id: Optional[int] = None):
        super().__init__(10, id)

        self.content = content
        
        self.__container_compatible__ = True

    def serialize(self):
        base_dict = super().serialize()
        base_dict["content"] = self.content

        return base_dict