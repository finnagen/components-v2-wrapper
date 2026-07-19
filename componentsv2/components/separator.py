from .base import ComponentV2

class Separator(ComponentV2):
    def __init__(self, divider: bool = None, spacing: int = None, id = None):
        if spacing != None and (spacing > 2 or spacing < 1):
            raise ValueError("Spacing can only be 1-2! 1: small padding, 2: large padding.")
        
        super().__init__(14, id)

        self.divider = divider
        self.spacing = spacing

        self.__container_compatible__ = True

    def serialize(self):
        base_dict = super().serialize()

        base_dict["divider"] = self.divider
        base_dict["spacing"] = self.spacing

        return base_dict