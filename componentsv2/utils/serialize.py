import nextcord

def serialize_emoji(emoji: nextcord.PartialEmoji):
    return {
        "name": emoji.name,
        "id": emoji.id,
        "animated": getattr(emoji, "animated", False)
    }