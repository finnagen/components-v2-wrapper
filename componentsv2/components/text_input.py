import nextcord
from .base import ComponentV2

class TextInput(ComponentV2):
    def __init__(self, custom_id: str, style: nextcord.TextInputStyle, min_length: int = None, max_length: int = None, required: bool = None, set_value: str = None, placeholder: str = None, id: int = None):
        super().__init__(4, id)

        self.custom_id = custom_id
        self.style = style
        self.min_length = min_length
        self.max_length = max_length

        self.required = required
        self.set_value = set_value
        self.placeholder = placeholder

    def serialize(self):
        base_dict = super().serialize()

        base_dict["custom_id"] = self.custom_id
        base_dict["style"] = self.style.value

        base_dict["min_length"] = self.min_length
        base_dict["max_length"] = self.max_length

        base_dict["required"] = self.required
        base_dict["value"] = self.set_value

        base_dict["placeholder"] = self.placeholder

        return base_dict