import nextcord

from typing import Optional
from .base import ComponentV2

from ..utils.serialize import serialize_emoji

class ButtonV2(ComponentV2):
    def __init__(self, style: nextcord.ButtonStyle, label: Optional[str] = None, custom_id: Optional[str] = None, url: Optional[str] = None, disabled: Optional[bool] = False, emoji: Optional[nextcord.PartialEmoji] = None, row: Optional[int] = 1, id: Optional[int] = None):
        if style != nextcord.ButtonStyle.link and custom_id == None:
            raise TypeError("Non-link buttons must have a custom_id attribute!")
        
        if style == nextcord.ButtonStyle.link and (custom_id != None or url == None):
            raise TypeError("Link buttons cannot have a custom_id and must have a url attribute!")
        
        super().__init__(2, id)

        self.row = row

        self.label = label
        self.emoji = emoji

        self.custom_id = custom_id
        self.url = url

        self.style = style.value

        self.disabled = disabled

        self.callback = None
        self.registered = False

    def __call__(self, func):
        if self.registered == True:
            raise ValueError("Buttons cannot be registered to multiple callbacks!")
        
        self.callback = func
        self.registered = True

        return self

    def serialize(self):
        base_dict: dict = super(ButtonV2, self).serialize()

        base_dict["label"] = self.label

        base_dict["custom_id"] = self.custom_id
        base_dict["url"] = self.url

        base_dict["style"] = self.style

        base_dict["disabled"] = self.disabled

        if self.emoji != None:
            base_dict["emoji"] = serialize_emoji(self.emoji)

        return base_dict
    
    async def activated(self, interaction):
        if self.disabled == True:
            return
        
        if self.registered == False:
            raise ValueError("Attempted to activate button, but it is not registered to a callback!")
        
        await self.callback(self.parent_holder, self, interaction)

class UIButtonV2(ButtonV2):
    def __init__(self, style, label = None, custom_id = None, url = None, disabled = False, emoji = None, row = 1, id = None):
        super().__init__(style, label, custom_id, url, disabled, emoji, row, id)

    async def activated(self, interaction):
        if self.disabled == True:
            return
        
        await self.ui_callback(interaction)

    async def ui_callback(self, interaction):
        pass