from nextcord import UnfurledMedia

from .base import ComponentV2

class MediaItem():
    def __init__(self, media: UnfurledMedia, description: str = None, spoiler: bool = None):
        self.media = media
        self.description = description
        self.spoiler = spoiler

    def serialize(self):
        return {
            "media": self.media.to_dict(),
            "description": self.description,
            "spoiler": self.spoiler,
        }

class Thumbnail(ComponentV2, MediaItem):
    def __init__(self, media: UnfurledMedia, description: str = None, spoiler: bool = None, id: int = None):
        ComponentV2.__init__(self, 11, id)
        MediaItem.__init__(self, media, description, spoiler)

    def serialize(self):
        base_dict = super().serialize()

        base_dict["media"] = self.media.to_dict()
        base_dict["description"] = self.description
        base_dict["spoiler"] = self.spoiler

        return base_dict
    
class File(ComponentV2, MediaItem):
    def __init__(self, file: UnfurledMedia, id = None):
        ComponentV2.__init__(13, id)
        MediaItem.__init__(self, file)

        self.__container_compatible__ = True

    def serialize(self):
        return {
            "file": self.media.to_dict(),
            "description": self.description,
            "spoiler": self.spoiler,
        }