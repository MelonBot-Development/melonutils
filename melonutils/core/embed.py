from concurrent.futures import process
from re import L
from tkinter import Image
from typing import List, Dict, Union, Optional

from discord import Embed as DPYEMBED
from discord import Member, User, ClientUser, Color

from .object import *
from .exceptions import *

ANY_USER = Union[User, Member, ClientUser]

class Embed(DPYEMBED):
    def __init__(
        self,
        embed_type: Optional[EmbedType] = EmbedType.Rich,
        title: Optional[str] = None,
        url: Optional[str] = None,
        description: Optional[str] = "",
        color: Optional[Color] = Color.blurple(),
        timestamp: Optional[datetime] = None,
        author: Optional[Union[AuthorObject, Dict[str, str], None]] = None,
        footer: Optional[Union[FooterObject, Dict[str, str], None]] = None,
        thumbnail: Optional[Union[ThumbnailObject, Dict[str, Union[str, int]], None]] = None,
        image: Optional[Union[ThumbnailObject, Dict[str, Union[str, int]], None]] = None,
        provider: Optional[Union[ProviderObject, Dict[str, Any]]] = None,
        fields: Optional[Union[Fields, List[Field]]] = None
    ):
        self._type: EmbedType = embed_type if embed_type in EmbedType else EmbedType.from_valye(embed_type)
        self._title: str = process_title(title)
        self._url: str = url if validate_url(url) else None
        self._description: str = process_desc(description)
        
        if isinstance(color, Color):
            self._color = color
        elif isinstance(color, str):
            color = getattr(Color, color, None)
            if isinstance(color, classmethod):
                self._color = color()
            else:
                self._color = Color.blurple()
                raise ValueError("Invalid color key is passed.")
            
        self._timestamp: datetime = timestamp if type(timestamp) == datetime else None
        self._author: AuthorObject = author if isinstance(author, AuthorObject) else AuthorObject.fromDict(author)
        self._footer: FooterObject = footer if isinstance(footer, FooterObject) else FooterObject.fromDict(footer)
        self._thumbnail: ImageObject = thumbnail if isinstance(thumbnail, ImageObject) else ImageObject.fromDict(thumbnail)
        self._image: ImageObject = image if isinstance(image, ImageObject) else ImageObject.fromDict(image)
        self._provider: ProviderObject = provider if isinstance(provider, ProviderObject) else ProviderObject.fromDict(provider)
        self._fields: Fields = Fields.fromDict(fields)
        
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str) -> NoReturn:
        self._title = process_title(value)
        
    @property
    def type(self) -> EmbedType:
        return self._type

    @type.setter
    def type(self, value: str) -> NoReturn:
        self._type = EmbedType.from_value(value)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> NoReturn:
        if check_desc(value):
            self._description = value

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Color) -> NoReturn:
        if isinstance(value, Color):
            self._color = value
        else:
            self._color = process_color(value) # type: ignore

    @property
    def author(self) -> AuthorObject:
        return self._author

    @author.setter
    def author(self, value: AuthorObject) -> NoReturn:
        self._author = AuthorObject.fromDict(value)

    @property
    def footer(self) -> Dict[str, str]:
        return self._footer

    @footer.setter
    def footer(self, value: Dict[str, str]) -> NoReturn:
        self._footer = FooterObject.fromDict(value)

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value) -> NoReturn:
        if isinstance(value, datetime):
            self._timestamp = value
        else:
            raise TypeError("Timestamp object must be an instance of datetime")

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value) -> NoReturn:
        if validate_url(value):
            self._url = value

    @property
    def thumbnail(self) -> ImageObject:
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value: Union[ImageObject, str]) -> NoReturn:
        try:
            self._thumbnail = ImageObject.fromDict(value)
        except:
            if validate_url(value):
                self._thumbnail = ImageObject(url=value)
            else:
                raise

    @property
    def image(self) -> ImageObject:
        return self._image

    @image.setter
    def image(self, value: Union[ImageObject, str]) -> NoReturn:
        try:
            self._image = ImageObject.fromDict(value)
        except:
            if validate_url(value):
                self._image = ImageObject(url=value)
            else:
                raise

    @property
    def fields(self) -> List[Field]:
        return self._fields

    @fields.setter
    def fields(self, value: List[Field]) -> NoReturn:
        self._fields = Fields.fromDict(value)

        if check_fields(value):  # type: ignore
            self._fields.extend(value)