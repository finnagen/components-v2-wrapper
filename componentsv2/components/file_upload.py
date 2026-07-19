import nextcord
from nextcord import Interaction

from .base import ComponentV2
from .gallery import MediaGallery as Gallery
from .media import MediaItem

def get_files(self, interaction, files: list[str]) -> list[MediaItem]: ## works for all files
    resolved = interaction.data.get("resolved")
    attachments: dict[str] = resolved.get("attachments")

    links = []
    for id in files:
        data = attachments.get(id)
        if data:
            links.append(data.get("url"))

    media = []

    for link in links:
        item = MediaItem(
            nextcord.UnfurledMedia(link)
        )
            
        media.append(item)

    return media

def get_gallery(self, interaction: Interaction, files: list[str]) -> Gallery: ## this only works for images
    media = get_files(self, interaction, files)
    return Gallery(media)

class FileUpload(ComponentV2):
    def __init__(self, custom_id: str, min_values: int = None, max_values: int = None, required: bool = True, id = None):
        if min_values and (min_values < 0 or min_values > 10):
            raise ValueError("min_values must be between 0-10.")
        
        if max_values and (max_values < 1 or max_values > 10):
            raise ValueError("max_values must be between 1-10.")

        if required == True and min_values and min_values < 1:
            raise ValueError("min_values must be ommited or >= 1 when required is omitted or True!")

        super().__init__(19, id)

        self.custom_id = custom_id
        self.min_values = min_values
        self.max_values = max_values
        self.required = required

    def serialize(self):
        base_dict = super().serialize()

        base_dict["min_values"] = self.min_values
        base_dict["max_values"] = self.max_values
        base_dict["custom_id"] = self.custom_id
        base_dict["required"] = self.required

        return base_dict