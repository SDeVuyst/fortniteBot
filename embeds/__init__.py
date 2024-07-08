import discord
from datetime import datetime
from helpers import ArtBuilder


DEFAULT_COLOR = 0xF4900D
ERROR_COLOR = 0xE02B2B
SUCCES_COLOR = 0x39AC39



class OperationFailedEmbed(discord.Embed):
    def __init__(self, title, description=None, emoji="❌", user=None):
        super().__init__(
            title=f"{emoji} {title}", 
            description=description,
            color=ERROR_COLOR,
            timestamp=datetime.now()
        )



class OperationSucceededEmbed(discord.Embed):
    def __init__(self, title, description=None, emoji="✅", user=None):
        super().__init__(
            title=f"{emoji} {title}",
            description=description,
            color=SUCCES_COLOR,
            timestamp=datetime.now(),
        )



class RedBorderEmbed(discord.Embed):
    def __init__(self, title, description=None, user=None):
        super().__init__(
            title=f"{title}",
            description=description,
            color=ERROR_COLOR,
            timestamp=datetime.now(),  
        )



class DefaultEmbed(discord.Embed):

    def __init__(self, title, description=None, user=None):
        super().__init__(
            title=f"{title}",
            description=description,
            color=DEFAULT_COLOR,
            timestamp=datetime.now(),
        )
