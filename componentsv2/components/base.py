from typing import Optional

class ComponentV2():
    def __init__(self, type: int, id: Optional[int] = None):
        self.type = type
        self.id = id

        self.value = None
        self.values = None

    @property
    def __discord_ui_model_type__(self):
        return True

    def serialize(self) -> dict:
        return {
            "type": self.type,
            "id": self.id,
        }