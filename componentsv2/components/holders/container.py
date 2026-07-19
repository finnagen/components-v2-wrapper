from .nestable import Nestable
from ..base import ComponentV2

from ..action_row import ActionRow

from typing import Optional

class Container(Nestable):
    def __init__(self, components: list[ComponentV2] = [], accent_color: int = None, spoiler: bool = None, id: Optional[int] = None):
        for component in components:
            if hasattr(component, "__container_compatible__") == False:
                raise TypeError(f"Component {component.__class__.__name__} not accepted in Containers!")
        
        super().__init__(17, id, components)
        
        self.accent_color = accent_color
        self.spoiler = spoiler
        
    def get_row(self, row: int) -> tuple[int, ActionRow]:
        total_rows = -1

        for component in self.components:
            if isinstance(component, ActionRow) and total_rows == row:
                return total_rows, component
            elif isinstance(component, ActionRow):
                total_rows += 1

        return total_rows, None 

    def append_component(self, component: ComponentV2): # chained
        if hasattr(component, "row"):
            row, action_row = self.get_row(component.row)

            if action_row != None:
                action_row.append_component(component)
                return self
            elif row + 1 == component.row:
                action_row = ActionRow()
                action_row.append_component(component)

                return self.append_component(action_row)
            else:
                IndexError("Action rows must be created sequentially!")

        self.components.append(component)

        return self

    def serialize(self):
        base_dict = super().serialize()

        base_dict["accent_color"] = self.accent_color
        base_dict["spoiler"] = self.spoiler

        return base_dict