import nextcord
from nextcord import Interaction

from .base import ComponentV2
from ..utils.serialize import serialize_emoji

class DefaultValue():
    def __init__(self, id: str, type: str):
        self.id = id
        self.type = type

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type
        }

class SelectObject(ComponentV2):
    def __init__(self, type: int, custom_id: str, placeholder: str = None, min_values: int = None, max_values: int = None, required: bool = True, disabled: bool = False, row: int = 0, id: int = None):
        if min_values != None and required == True and min_values < 1:
            raise ValueError("Required cannot be true if min_values is less than 1!")
        
        super().__init__(type, id)
        
        self.custom_id = custom_id
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.required = required
        self.disabled = disabled
        self.row = row

        self.callback = None
        self.registered = False

    def serialize(self):   
        return {
            "type": self.type,
            "id": self.id,
            "custom_id": self.custom_id,
            "placeholder": self.placeholder,
            "min_values": self.min_values,
            "max_values": self.max_values,
            "required": self.required,
            "disabled": self.disabled
        }
    
    def __call__(self, func):
        if self.registered == True:
            raise ValueError("Cannot register a Select component to multiple callbacks!")
        
        self.registered = True
        self.callback = func

        return self
    
    def on_submit(self, func):
        if self.registered == True:
            raise ValueError("Cannot register a Select component to multiple callbacks!")
        
        self.registered = True
        self.callback = func

        return self

class StringSelect(SelectObject):
    class SelectOption():
        def __init__(self, label: str, value: str, description: str = None, emoji: nextcord.PartialEmoji = None, default: bool = False):
            self.label = label
            self.value = value
            self.description = description
            self.emoji = emoji
            self.default = default

        def serialize(self):
            emoji = None if self.emoji == None else serialize_emoji(self.emoji)
            return {
                "label": self.label,
                "value": self.value,
                "description": self.description,
                "default": self.default,
                "emoji": emoji,
            }


    def __init__(self, custom_id: str, options: list[SelectOption], placeholder: str = None, min_values: int = None, max_values: int = None, required: bool = True, disabled: bool = False, row: int = 0, id: int = None):
        super().__init__(3, custom_id, placeholder, min_values, max_values, required, disabled, row, id)
        
        self.options = options
        self.placeholder = placeholder

    def serialize(self):   
        str_options: list[dict[str]] = []
        for option in self.options:
            str_options.append(option.serialize())
        
        base_dict = super().serialize()
        base_dict["options"] = str_options

        return base_dict

    async def activated(self, interaction: Interaction):
        if self.disabled == True:
            return
        
        if self.registered == False:
            raise ValueError("Attempted to activate Select component, but it is not registered to a callback!")
        
        values = interaction.data.get("values")
        
        await self.callback(self.parent_holder, self, interaction, values)

## DEFAULT VALUE OBJECTS (might create ANOTHER subclass to handle these fellas)
class UserSelect(SelectObject):
    def __init__(self, custom_id: str, default_values: list[DefaultValue] = None, placeholder: str = None, min_values: int = None, max_values: int = None, required: bool = True, disabled: bool = False, row: int = 0, id: int = None):
        if default_values != None:
            values = len(default_values)

            min = min_values or 1
            max = max_values or 1

            if min > values or max < values:
                raise ValueError("The length of 'default_values' MUST be within the range of min_values and max_values (default 1-1).")
        
        super().__init__(5, custom_id, placeholder, min_values, max_values, required, disabled, row, id)
        
        self.default_values = default_values
        self.placeholder = placeholder

    def serialize(self):   
        if self.default_values != None:
            str_values: list[dict[str]] = []
            for value in self.default_values:
                str_values.append(value.serialize())
        else:
            str_values = None
            
        base_dict = super().serialize()
        base_dict["default_values"] = str_values

        return base_dict

    async def activated(self, interaction: Interaction):
        if self.disabled == True:
            return
        
        if self.registered == False:
            raise ValueError("Attempted to activate Select component, but it is not registered to a callback!")
        
        values = interaction.data.get("values")
        await self.callback(self.parent_holder, self, interaction, values) ## due to a nextcord limitation, i am only able to send the list of ids, not user objects.

class RoleSelect(SelectObject):
    def __init__(self, custom_id: str, default_values: list[DefaultValue] = None, placeholder: str = None, min_values: int = None, max_values: int = None, required: bool = True, disabled: bool = False, row: int = 0):
        if default_values != None:
            values = len(default_values)

            min = min_values or 1
            max = max_values or 1

            if min > values or max < values:
                raise ValueError("The length of 'default_values' MUST be within the range of min_values and max_values (default 1-1).")
        
        super().__init__(6, custom_id, placeholder, min_values, max_values, required, disabled, row, id)
        
        self.default_values = default_values
        self.placeholder = placeholder

    def serialize(self):   
        if self.default_values != None:
            str_values: list[dict[str]] = []
            for value in self.default_values:
                str_values.append(value.serialize())
        else:
            str_values = None
            
        base_dict = super().serialize()
        base_dict["default_values"] = str_values

        return base_dict

    async def activated(self, interaction: Interaction):
        if self.disabled == True:
            return
        
        if self.registered == False:
            raise ValueError("Attempted to activate Select component, but it is not registered to a callback!")
        
        values = interaction.data.get("values")
        await self.callback(self.parent_holder, self, interaction, values) ## due to a nextcord limitation, i am only able to send the list of values, not user objects.

class MentionableSelect(SelectObject):
    def __init__(self, custom_id: str, default_values: list[DefaultValue] = None, placeholder: str = None, min_values: int = None, max_values: int = None, required: bool = True, disabled: bool = False, row: int = 0, id: int = None):
        if default_values != None:
            values = len(default_values)

            min = min_values or 1
            max = max_values or 1

            if min > values or max < values:
                raise ValueError("The length of 'default_values' MUST be within the range of min_values and max_values (default 1-1).")
        
        super().__init__(7, custom_id, placeholder, min_values, max_values, required, disabled, row, id)

        self.default_values = default_values
        self.placeholder = placeholder

    def serialize(self):   
        if self.default_values != None:
            str_values: list[dict[str]] = []
            for value in self.default_values:
                str_values.append(value.serialize())
        else:
            str_values = None
            
        base_dict = super().serialize()
        base_dict["default_values"] = str_values

        return base_dict

    async def activated(self, interaction: Interaction):
        if self.disabled == True:
            return
        
        if self.registered == False:
            raise ValueError("Attempted to activate Select component, but it is not registered to a callback!")
        
        values = interaction.data.get("values")
        await self.callback(self.parent_holder, self, interaction, values) ## due to a nextcord limitation, i am only able to send the list of values, not user objects.

class ChannelSelect(SelectObject):
    def __init__(self, custom_id: str, default_values: list[DefaultValue] = None, channel_types: list[nextcord.ChannelType] = None, placeholder: str = None, min_values: int = None, max_values: int = None, required: bool = True, disabled: bool = False, row: int = 0, id: int = None):
        if default_values != None:
            values = len(default_values)

            min = min_values or 1
            max = max_values or 1

            if min > values or max < values:
                raise ValueError("The length of 'default_values' MUST be within the range of min_values and max_values (default 1-1).")
            
        if channel_types != None:
            channel_values = []
            for type in channel_types:
                channel_values.append(type.value)
        else:
            channel_values = None

        self.channel_types = channel_values
        super().__init__(8, custom_id, placeholder, min_values, max_values, required, disabled, row, id)
        
        self.default_values = default_values
        self.placeholder = placeholder

    def serialize(self):   
        if self.default_values != None:
            str_values: list[dict[str]] = []
            for value in self.default_values:
                str_values.append(value.serialize())
        else:
            str_values = None
            
        base_dict = super().serialize()
        base_dict["default_values"] = str_values
        base_dict["channel_types"] = self.channel_types

        return base_dict

    async def activated(self, interaction: Interaction):
        if self.disabled == True:
            return
        
        if self.registered == False:
            raise ValueError("Attempted to activate Select component, but it is not registered to a callback!")
        
        values = interaction.data.get("values")
        await self.callback(self.parent_holder, self, interaction, values) ## due to a nextcord limitation, i am only able to send the list of values, not user objects.