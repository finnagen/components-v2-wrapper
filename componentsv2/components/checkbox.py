from .base import ComponentV2

class Checkbox(ComponentV2):
    def __init__(self, custom_id: str, default: bool = None, id = None):
        super().__init__(23, id)

        self.custom_id = custom_id
        self.default = default

    def serialize(self):
        base_dict = super().serialize()

        base_dict["custom_id"] = self.custom_id
        base_dict["default"] = self.default

        return base_dict
    
class CheckboxGroup(ComponentV2):
    class Option():
        def __init__(self, value: str, label: str, description: str = None, default: bool = None):
            self.value = value
            self.label = label

            self.description = description
            self.default = default

        def serialize(self):
            return {
                "value": self.value,
                "label": self.label,

                "description": self.description,
                "default": self.default,
            }

    def __init__(self, custom_id: str, options: list[Option], min_values: int = None, max_values: int = None, required: bool = None, id = None):
        super().__init__(22, id)

        if required == True and min_values and min_values < 1:
            raise ValueError("min_values must be ommited or >= 1 when required is omitted or True!")
        
        self.custom_id = custom_id
        self.options = options
        self.min_values = min_values
        self.max_values = max_values
        self.required = required

    def serialize(self):
        base_dict = super().serialize()

        checkbox_options = []

        for option in self.options:
            checkbox_options.append(option.serialize())

        base_dict["custom_id"] = self.custom_id
        base_dict["options"] = checkbox_options
        base_dict["min_values"] = self.min_values
        base_dict["max_values"] = self.max_values
        base_dict["required"] = self.required

        return base_dict