import nextcord
import json
import copy

from nextcord.ext import commands
from nextcord import Interaction
from typing import Optional

from nextcord import MessageFlags

## CLASSES
from .components.base import ComponentV2
from .components.action_row import ActionRow
from .components.button import ButtonV2

from .components.select import (
    StringSelect,
)

from .component_holder import (
    ComponentHolder,
    ModalV2,
)

from .components.holders.label import Label

class NextcordAPIWrapperV2():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.active_holders = {}
        self.active_modals = {}

        bot.add_listener(self.on_interaction, "on_interaction")

    async def on_interaction(self, interaction: Interaction):
        if interaction.type == nextcord.InteractionType.component:
            holder: ComponentHolder = self.active_holders.get(str(interaction.message.id))
            if holder != None:
                component = holder.get_component(interaction.data.get("custom_id"))
                if component != None:
                    await component.activated(interaction)
        elif interaction.type == nextcord.InteractionType.modal_submit:
            modal: ModalV2 = self.active_modals.get(interaction.user.id)
            if modal != None:
                await modal.submitted(interaction, interaction.data.get("components"))
    
    def __message_interaction_payload(self, components: list[ComponentV2], content: str = None, flags: int = None) -> dict[str]:
        return {
            "type": 4, # update your FUCKING docs discord
            "data": {
                "flags": flags,
                "content": content,
                "components": components
            }
        }

    def __edit_interaction_payload(self, components: list[ComponentV2], content: str = None) -> dict[str]:
        return {
            "type": 7, # update your FUCKING docs discord
            "data": {
                "content": content,
                "components": components
            }
        }
    
    async def send_modal(self, interaction: Interaction, modal: ModalV2):
        self.active_modals[interaction.user.id] = modal

        await self.bot.http.request(
            nextcord.http.Route("POST", f"/interactions/{interaction.id}/{interaction.token}/callback"),
            json = modal.serialize()
        )

    async def send_message(self, interaction: Interaction, component_holder: ComponentHolder, content: str = None, *, ephemeral: bool = False, is_components_v2: bool = False):
        if is_components_v2 == True and content != None:
            raise TypeError("ComponentsV2 messages cannot contain content!")
        
        flags = MessageFlags(ephemeral=ephemeral, is_components_v2=is_components_v2).value
        response = await self.bot.http.request(
            nextcord.http.Route("POST", f"/interactions/{interaction.id}/{interaction.token}/callback?with_response=true"),
            json=self.__message_interaction_payload(components=component_holder.serialize(), content=content, flags=flags)
        )

        self.active_holders[response["interaction"]["response_message_id"]] = component_holder

    async def send_followup(self, interaction: Interaction, component_holder: ComponentHolder, content: str = None, *, ephemeral: bool = False, is_components_v2: bool = False):
        if is_components_v2 == True and content != None:
            raise TypeError("ComponentsV2 messages cannot contain content!")

        flags = MessageFlags(ephemeral=ephemeral, is_components_v2=is_components_v2).value
        response = await self.bot.http.request(
            nextcord.http.Route("POST", f"/webhooks/{interaction.application_id}/{interaction.token}"),
            json={"components": component_holder.serialize(), "content": content, "flags": flags}
        )

        self.active_holders[response["id"]] = component_holder

    async def edit_message(self, interaction: Interaction, component_holder: ComponentHolder, content: str = None):
        await self.bot.http.request(
            nextcord.http.Route("POST", f"/interactions/{interaction.id}/{interaction.token}/callback"),
            json=self.__edit_interaction_payload(components=component_holder.serialize(), content=content)
        )