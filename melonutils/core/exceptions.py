from typing import Tuple

import discord
from redbot.core import commands # type: ignore

class RedBotException(discord.ClientException):
    """
    The base exception for the bot. 
    
    All other exceptions should inherit from this.
    """
    
    __slots__: Tuple[str, ...] = ()

class RedBotCommandError(commands.CommandError, RedBotException):
    """
    The base exception for the bot command errors.
    """
    
    __slots__: Tuple[str, ...] = ()
    
class HierarchyException(RedBotCommandError):
    """
    Raised when the bot is requested to perform an operation on a member
    that is higher than them in the guild hierarchy.
    """
    
    __slots__: Tuple[str, ...] = (
        "member",
        "author_error"
    )
    
    def __init__(
        self,
        member: discord.Member,
        *,
        author_error: bool = False
    ) -> None:
        self.member: discord.Member = member
        self.author_error: bool = author_error
        
        if author_error is False:
            super().__init__(
                f"**{member}**\'s top role is higher than mine. I can\'t do that!"
            )
        
        else:
            super().__init__(
                f"**{member}**\'s top role is higher than your top role. You can\'t do that!"
            )
    
class ActionNotExecutable(RedBotCommandError):
    """
    The exception for when an action is not executable.
    """
    
    def __init__(self, message):
        super().__init__("{}".format(message))
        