from nextcord import UnfurledMedia
from .base import ComponentV2
from.media import MediaItem

class MediaGallery(ComponentV2):
    def __init__(self, items: list[MediaItem], id = None):
        if len(items) < 1 or len(items) > 10:
            raise ValueError("List of Media Items must be within the range 1-10.")

        super().__init__(12, id)
        self.items = items

        self.__container_compatible__ = True

    def serialize(self):
        base_dict = super().serialize()

        items = []
        for media in self.items:
            items.append(media.serialize())
        
        base_dict["items"] = items

        return base_dict