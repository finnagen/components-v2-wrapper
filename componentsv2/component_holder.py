from .components.base import ComponentV2
from .components.button import ButtonV2
from .components.action_row import ActionRow
from .components.select import SelectObject

import copy
import asyncio

class ComponentHolder():
    def __init_subclass__(cls):
        children: list[ComponentV2] = []

        for base in reversed(cls.__mro__):
            children.extend(
                member
                for member in base.__dict__.values()
                if hasattr(member, "__discord_ui_model_type__")
            )

        if len(children) > 25:
            raise TypeError("Component Holders can only contain 25 components!")

        cls.children = children

    def __init__(self, timeout: int = None):
        self.children = copy.deepcopy(self.children)
        rows: list[ActionRow] = []

        for child in self.children:
            if hasattr(child, "parent_holder") == False:
                child.parent_holder = self

            if isinstance(child, ActionRow):
                rows.append(child)

        self.rows = rows

        self.parent_wrapper = None
        self.id = None

        for child in self.children:
            if isinstance(child, ButtonV2) or isinstance(child, SelectObject): # switch StringSelect to general Select object
                self.append_to_row(child.row, child)

        if timeout is not None:
            created_task = asyncio.create_task(self.__timeout(timeout))
            self.__task_timeout = created_task
        else:
            self.__task_timeout = None

        self.timeout = timeout

    async def __timeout(self, delay: int):
        await asyncio.sleep(delay)
        self.close()

    def __rec_add_components(self, component: ComponentV2, initial: bool):
        if hasattr(component, "row"):
            self.append_to_row(component.row, component)

        if hasattr(component, "parent_holder") == False:
            component.parent_holder = self
        elif isinstance(component.parent_holder, ComponentHolder):
            raise TypeError("Cannot re-assign components!")

        if hasattr(component, "accessory") == True:
            component.accessory.__row_child__ = True
            self.children.append(component.accessory)

        if initial == False:
            component.__row_child__ = True

        self.children.append(component)

        if hasattr(component, "components") == True:
            for child in component.components:
                self.__rec_add_components(child, False)

    def add_component(self, component: ComponentV2):
        self.__rec_add_components(component, True)
        return self

    def add_components(self, *args: ComponentV2):
        components = list(args)

        for component in components:
            self.__rec_add_components(component, True)

    def append_to_row(self, row: int, component: ComponentV2):
        if row < len(self.rows):
            action_row = self.rows[row]
        elif row == len(self.rows):
            action_row = ActionRow()
            self.rows.append(action_row)
            self.children.append(action_row)
        else:
            raise IndexError("New rows must be created sequentially (cannot skip rows).")

        component.__row_child__ = True
        action_row.append_component(component)

    def serialize(self):
        components = []

        for child in self.children:
            if hasattr(child, "__row_child__") == True:
                continue

            components.append(child.serialize())
        
        return components
    
    def get_component(self, custom_id: str):
        for child in self.children:
            if getattr(child, "custom_id", None) == custom_id:
                return child

    def close(self):
        if self.parent_wrapper is not None:
            del self.parent_wrapper.active_holders[self.id]

        self.parent_wrapper = None
        self.id = None

        if self.__task_timeout is not None:
            self.__task_timeout.cancel()
            self.__task_timeout = None
            
class ModalV2():
    def __init__(self, title: str, timeout: int = None, custom_id: str = None):
        
        self.custom_id = custom_id
        self.title = title

        self.children = []

        self.parent_wrapper = None
        self.id = None

        if timeout is not None:
            created_task = asyncio.create_task(self.__timeout(timeout))
            self.__task_timeout = created_task
        else:
            self.__task_timeout = None

        self.timeout = timeout

    async def __handle_component_submitted(self, sc: dict[str]):
        if custom_id := sc.get("custom_id"):
            component = self.get_component(custom_id)

            if component is not None:
                if values := sc.get("values"):
                    component.values = values
                else:
                    values = None

                if (value := sc.get("value")) is not None:
                    component.value = value
                elif values:
                    component.value = values[0]

        if component := sc.get("component"):
            await self.__handle_component_submitted(component)

        if components := sc.get("components"):
            for child in components:
                await self.__handle_component_submitted(child)

    async def submitted(self, interaction, ser_components: list[dict[str]], initial: bool = True):
        for sc in ser_components:
            await self.__handle_component_submitted(sc)
        
        if initial == True:
            await self.on_form_submit(interaction)

    def on_submit_decorator(self, func):
        self.on_form_submit = func

    async def on_form_submit(self, interaction):
        pass

    def __rec_add_components(self, component: ComponentV2, initial: bool):
        if hasattr(component, "parent_holder") == False:
            component.parent_holder = self
        elif isinstance(component.parent_holder, ModalV2):
            raise TypeError("Cannot re-assign components!")

        if hasattr(component, "accessory") == True:
            component.accessory.__row_child__ = True
            self.children.append(component.accessory)

        if initial == False:
            component.__row_child__ = True

        self.children.append(component)

        if hasattr(component, "components") == True:
            for child in component.components:
                self.__rec_add_components(child, False)

        if hasattr(component, "component") == True:
            self.__rec_add_components(component.component, False)

    def add_component(self, component: ComponentV2):
        self.__rec_add_components(component, True)
        return self

    def add_components(self, *args: ComponentV2):
        components = list(args)

        for component in components:
            self.__rec_add_components(component, True)

    def serialize(self):
        components = []

        for child in self.children:
            if hasattr(child, "__row_child__") == True:
                continue

            components.append(child.serialize())
        
        return {
            "type": 9,
            "data": {
                "custom_id": self.custom_id,
                "title": self.title,
                "components": components
            }
        }
    
    def get_component(self, custom_id: str):
        if custom_id == None:
            return

        for child in self.children:
            if getattr(child, "custom_id", None) == custom_id:
                return child
            
    def get_components(self) -> list[ComponentV2]:
        components = []

        for child in self.children:
            if hasattr(child, "__row_child__") == True:
                continue

            components.append(child)

        return components

    def close(self):
        if self.parent_wrapper is not None:
            del self.parent_wrapper.active_modals[self.id]

        self.parent_wrapper = None
        self.id = None

        if self.__task_timeout is not None:
            self.__task_timeout.cancel()
            self.__task_timeout = None