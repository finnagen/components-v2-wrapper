from ..base import ComponentV2

class Label(ComponentV2):
    def __init__(self, label: str, component: ComponentV2, description: str = None, id: int = None):
        super().__init__(18, id)

        self.label = label

        self.component = component
        self.description = description

    def serialize(self):
        base_dict = super().serialize()

        base_dict["label"] = self.label
        base_dict["component"] = self.component.serialize()
        base_dict["description"] = self.description

        return base_dict