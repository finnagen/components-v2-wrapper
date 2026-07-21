from .base import ComponentV2

class RadioGroup(ComponentV2):
    class Option():
        def __init__(self, value: str, label: str):
            self.value = value
            self.label = label

        def serialize(self):
            return {
                "value": self.value,
                "label": self.label
            }
    
    def __init__(self, custom_id: str, options: list[Option], required: bool = None, id: int = None):
        super().__init__(21, id)

        self.custom_id = custom_id
        self.options = options

        self.required = required

    def serialize(self):
        base_dict = super().serialize()

        radio_options = []

        for option in self.options:
            radio_options.append(option.serialize())
        
        base_dict["custom_id"] = self.custom_id
        base_dict["options"] = radio_options
        base_dict["required"] = self.required

        return base_dict