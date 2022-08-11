from __future__ import annotations

import io, os, re, aiohttp, asyncio, logging
from time import time_lib
from datetime import datetime
from typing import TYPE_CHECKING, TypeVar, Callable, Awaitable, Union, Any, Optional, Tuple

import discord
from redbot.core import commands # type: ignore

try:
    from typing import ParamSpec # type: ignore
except ImportError:
    from typing_extensions import ParamSpec
    
from .exceptions import *
    
T = TypeVar("T")
P = ParamSpec("P")
BE = TypeVar("BE", bound="discord.guild.BanEntry")

CDN = re.complite(
    r'(https?://)?(media|cdn)\.discord(app)?\.(com|net)/attachments/'
    r'(?P<channel_id>[0-9]+)/(?P<message_id>[0-9]+)/(?P<filename>[\S]+)'
)
URL_REGEX = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|%[0-9a-fA-F][0-9a-fA-F])+')

__all__: Tuple[str, ...] = (
    ""
)

def ascii_color(color=None, /, *, fmt=0, bg=False) -> str:
    """
    Returns the ascii color escape string for the given number.
    
    :param color: The color number.
    :param fmt: The format number.
    :param bg: Whether to return as a background color
    """
    base = "\u001b["
    
    if fmt != 0:
        base += "{fmt};"
    
    if color is None:
        base += "{color}m"
        color = 0
    
    else:
        if bg is True:
            base += "4{color}m"
        
        else:
            base += "3{color}m"
    
    return base.format(fmt=fmt, color=color)

def markdown_remove(entity: Any) -> str:
    """
    Returns the string of an object with discord markdown removed.
    
    Parameters
    ----------
    entity: Any
        The object to remove markdown from.
    
    Returns
    -------
    str
        The string of the object with markdown removed.
    """
    return discord.utils.remove_markdown(discord.utils.escape_mentions(str(entity)))

def codeblock_wrapper(text: str, /, *, lang: str = "py"):
    """
    Wraps a string into a code-block, and adds zero width
    characters to avoid the code block getting cut off.
    
    Parameters
    ----------
    text: str
        The text to wrap.
    lang: str
        The code language to use.
    
    Returns
    -------
    str
        The wrapped text.
    """
    text = text.replace("`", "\u200b`")
    return f"```{lang}\n{text}\n```"

def safe_reason(
    author: Union[discord.Member, discord.User], 
    reason: str, 
    *, 
    length: int = 512
) -> str:
    base = f"Action by {author} ({author.id}) for: "
    
    length_limit = length - len(base)
    
    if len(reason) > length_limit:
        reason = reason[: length_limit - 3] + "..."
        
    return base + reason

def format_date(
    date: datetime
) -> str:
    """
    Formats a date to a string in the preferred way.
    
    Parameters
    ----------
    date: datetime.datetime
        The date to format.
    
    Returns
    -------
    str
        The formatted date.
    """
    return date.strftime("%b %d, %Y %H:%M %Z")

def add_logging(
    func: Callable[P, Union[Awaitable[T], T]] # type: ignore
) -> Callable[P, Union[Awaitable[T], T]]: # type: ignore
    """
    Adds logging to a coroutine or a function.
    
    .. code-block:: python3
    
        >>> async def foo(a: int, b: int) -> int:
        >>>     return a + b
    
        >>> logger = add_logging(foo)
        >>> result = await logger(1, 2)
        >>> print(result)
        3
    
        >>> def foo(a: int, b: int) -> int:
        >>>     return a + b
    
        >>> logger = add_logging(foo)
        >>> result = logger(1, 2)
        >>> print(result)
        3
    """
    
    async def _async_wrapped(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> Awaitable[T]:
        start = time_lib.time()
        
        result = await func(*args, **kwargs)
        
        print(f"{func.__name__} took {time_lib.time() - start:.2f} seconds")
        
        return result
    
    def _sync_wrapped(
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:
        start = time_lib.time()
        
        result = func(*args, **kwargs)
        
        print(f'{func.__name__} took {time_lib.time() - start:.2f} seconds')
        
        return result
    
    return _async_wrapped if asyncio.iscoroutinefunction(func) else _sync_wrapped # type: ignore

async def can_execute_action(
    ctx: commands.Context,
    target: Union[discord.Member, discord.User],
    *,
    fail_if_not_upgrade: bool = True,
) -> Optional[bool]:
    """
    |coro|
    
    A wrapped predicate to check if the action can be executed.
    
    Parameters
    ----------
    ctx: :class:`commands.Context`
        The context of the command.
    target: Union[:class:`discord.Member`, :class:`discord.User`]
        The target of the action.
    fail_if_not_upgrade: :class:`bool`
        Whether to fail if the user can't be upgraded to a Member.
    
    Returns
    -------
    Optional[:class:`bool`]
        Whether the action can be executed.
    
    Raises
    ------
    HierarchyException
        The action cannot be executed due to role hierarchy.
    ActionNotExecutable
        The action cannot be executed due to other reasons.
    commands.NoPrivateMessage
        This command cannot be used in private messages.
    """
    guild = ctx.guild
    
    if guild is None or not isinstance(ctx.author, discord.Member):
        raise commands.NoPrivateMessage('This command cannot be used in private messages.')
    
    if isinstance(target, discord.User):
        upgraded = await ctx.bot.get_or_fetch_member(guild, target)
        
        if upgraded is None:
            if fail_if_not_upgrade:
                raise ActionNotExecutable("That user is not a member of this server.")
            
        else:
            target = upgraded
            
    if ctx.author == target:
        raise ActionNotExecutable("You cannot execute this action on yourself!")
    
    if guild.owner == target:
        raise ActionNotExecutable("I cannot execute any action on the server owner!")
    
    if isinstance(target, discord.Member):
        if guild.me.top_role <= target.top_role:
            raise HierarchyException(target)
        
        if guild.owner == ctx.author:
            return
        
        if ctx.author.top_role <= target.top_role:
            raise HierarchyException(target, author_error=True)
