import json
from typing import Tuple, Dict, Any

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
        
class EmbedGenException(Exception):
    @property
    def msg(self) -> str:
        return self._msg
    
    def __init__(
        self,
        msg="An exception was occured during EmbedGen operations.",
        *args,
        **kwargs
    ):
        self._msg = msg
        super().__init__(*args)
        
    def __str__(self) -> str:
        return self.msg
    
    def __repr__(self) -> str:
        return self.__str__()
    
class UnexpectedKwargsError(EmbedGenException):
    def __init__(
        self,
        unexpected_kwargs: Dict[str, Any],
        *args,
        **kwargs
    ):
        if "msg" in kwargs.keys():
            kwargs.pop("msg")
        
        self.kwargs = unexpected_kwargs
        
        msg = (
            "`EmbedGen.__init__()` caught unexpected keyword arguments! : "
            f"{json.dumps(obj=self.kwargs, indent=4, ensure_ascii=False)}"
        )
        super().__init__(*args, msg=msg, **kwargs)
        
class InvalidColorError(EmbedGenException):
    def __init__(
        self,
        invalid_color,
        *args,
        **kwargs
    ):
        self.color = invalid_color
        
        if "msg" in kwargs.keys():
            kwargs.pop("msg")
            
        super().__init__(
            *args,
            msg="Embed color must be an instance of `discord.Color`! : ",
            **kwargs
        )
        
class InvalidFieldError(EmbedGenException):
    def __init__(
        self,
        invalid_field,
        *args,
        **kwargs
    ):
        self.field = invalid_field
        
        if "msg" in kwargs.keys():
            kwargs.pop("msg")
            
        super().__init__(
            *args,
            msg="Embed field must have structure of `{'name': name, 'value': value}`",
            **kwargs
        )
        