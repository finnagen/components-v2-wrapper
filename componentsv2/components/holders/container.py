from .nestable import Nestable
from ..base import ComponentV2

from ..action_row import ActionRow
from ..text_display import TextDisplay

from typing import Optional

class Container(Nestable):
    def __init__(self, components: list[ComponentV2] = None, accent_color: int = None, spoiler: bool = None, id: Optional[int] = None, push_to_front: bool = False):
        if components is None:
            components = []

        for component in components:
            if hasattr(component, "__container_compatible__") == False:
                raise TypeError(f"Component {component.__class__.__name__} not accepted in Containers!")
        
        super().__init__(17, id, components)
        
        self.accent_color = accent_color
        self.spoiler = spoiler

        self.push_to_front = push_to_front
        self.footer = None
        
    def get_row(self, row: int) -> tuple[int, ActionRow]:
        total_rows = -1

        for component in self.components:
            if isinstance(component, ActionRow):
                total_rows += 1

            if isinstance(component, ActionRow) and total_rows == row:
                return total_rows, component

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
                raise IndexError("Action rows must be created sequentially!")

        self.components.append(component)

        if self.footer is not None:
            self.components.remove(self.footer)
            self.components.append(self.footer)

        return self
    
    def add_field(self, title: str, content: str):
        return self.append_component(
            TextDisplay(
                f"**{title}**\n{content}"
            )
        )

    def set_footer(self, footer: str):
        if self.footer is not None:
            self.components.remove(self.footer)

        self.footer = TextDisplay(f"-# {footer}")
        self.components.append(
            self.footer
        )

        return self

    def serialize(self):
        base_dict = super().serialize()

        base_dict["accent_color"] = self.accent_color
        base_dict["spoiler"] = self.spoiler

        return base_dict