import re
from enum import Enum
from datetime import datetime
from abc import abstractmethod
from typing import Dict, Optional, List, Union, NoReturn, Any

from discord import Color

def validate_url(value) -> bool:
    return isinstance(value, str) and re.match("^https?", value)

@DeprecationWarning
class EmbedType(Enum):
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"

    def __contains__(self, item):
        """
        Override `in` keyword to check Embed`s type value.
        
        :param item:
        :return:
        """
        if type(item) == self.__class__:
            return super(EmbedType, self).__contains__(item)

        return str(item) in EmbedType.__members__.keys()

    @classmethod
    def from_value(cls, value: Union[str, EmbedType]) -> Union[EmbedType, NoReturn]: # type: ignore
        if type(value) == cls:
            return value

        elif type(value) == str:
            try:
                return EmbedType[value.upper()]
            except KeyError:
                raise KeyError("Unknown Embed Type {}".format(value))

        raise ValueError("EmbedType enum can be constructed only using string key or EmbedType object.")

class EmbedObject(object):
    """
    Represents property object used in discord`s embed structure.
    """

    def __repr__(self) -> str:
        return f"Embed.Object"

    @classmethod
    @abstractmethod
    def fromDict(cls, data: Dict[str, Any]):
        if not isinstance(data, dict):
            raise TypeError("Expected Dict[str, Any], caught {}".format(data.__class__))
        if cls == EmbedObject:
            raise NotImplementedError("Subclasses should implement the method!")

    @abstractmethod
    def toDict(self) -> dict:
        raise NotImplementedError("Subclasses should implement the method!")

@DeprecationWarning
class EmptyObject(EmbedObject):
    """
    Represents `empty` value in embed property.
    """

    def __init__(self, property_name: str, optional: bool = False) -> None:
        self.property_name = property_name
        self.optional = optional

    @classmethod
    def fromDict(cls, data: Dict[str, Union[str, bool]]) -> EmptyObject: # type: ignore
        return cls(
            property_name=data.get("property_name"),
            optional=data.get("optional") or True
        )

    def toDict(self) -> dict:
        raise ValueError("Empty object cannot be serialized into json.")

    def __str__(self) -> Union[str, NoReturn]:
        if not self.optional:
            raise ValueError(
                "Embed property '{}' cannot be empty!".format(self.property_name)
            )
        else:
            return "Embed property {} is empty.".format(self.property_name)

    def __repr__(self) -> str:
        return "Embed.Empty(property_name={},optional={})".format(self.property_name, self.optional)

    def __len__(self) -> int:
        """
        Tool to check whether property is empty or not.
        
        :return: Always 0, because this class always represents empty value.
        """
        return 0

    def __bool__(self) -> bool:
        """
        Tool to check whether property is empty or not.
        
        :return: Always False, because this class always represents empty value.
        """
        return False


class AuthorObject(EmbedObject):
    """
    Represents author objects on discord Embed.
    """

    def __init__(
        self, 
        name: str, 
        url: Optional[str] = None, 
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None
    ):
        if type(name) != str or len(name) > 256:
            raise ValueError("Author Object cannot have name longer than 256.")
        self.name = name

        if url is not None and validate_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        if icon_url is not None and validate_url(icon_url):
            self.icon_url = icon_url
        else:
            raise ValueError("Invalid icon url!")

        if proxy_icon_url is not None and validate_url(proxy_icon_url):
            self.proxy_icon_url = proxy_icon_url
        else:
            raise ValueError("Invalid proxy icon url!")

    @classmethod
    def fromDict(cls, data: Union["AuthorObject", Dict[str, Any]]) -> AuthorObject: # type: ignore
        if not isinstance(data, dict):
            raise TypeError("Expected Dict[str, Any], caught {}".format(data.__class__))
        name = data.get("name")
        url = data.get("url") or None
        icon_url = data.get("icon_url") or None
        proxy_icon_url = data.get("proxy_icon_url") or None

        return cls(
            name=name,
            url=url,
            icon_url=icon_url,
            proxy_icon_url=proxy_icon_url
        )

    def toDict(self) -> Dict[str, str]:
        result = {
            "name": self.name
        }
        if self.url:
            result["url"] = self.url
        if self.icon_url:
            result["icon_url"] = self.icon_url
        if self.proxy_icon_url:
            result["proxy_icon_url"] = self.proxy_icon_url
        return result

    def __str__(self) -> str:
        return str(self.toDict())

    def __repr__(self) -> str:
        return ("Embed.Author(name={},url={},icon_url={},proxy_icon_url={})"
                .format(self.name, self.url, self.icon_url, self.proxy_icon_url))

class FooterObject(EmbedObject):
    """
    Represents footer objects on discord Embed.
    """
    
    def __init__(
        self, 
        text: Optional[str], 
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None
    ):
        self.text = text
        self.icon_url = icon_url if validate_url(icon_url) else None
        self.proxy_icon_url = proxy_icon_url if validate_url(proxy_icon_url) else None

        if proxy_icon_url is not None and validate_url(proxy_icon_url):
            self.proxy_icon_url = proxy_icon_url

    @classmethod
    def fromDict(
        cls, 
        data: Dict[str, Any]
    ) -> FooterObject: # type: ignore
        if not isinstance(data, dict):
            raise TypeError("Expected Dict[str, Any], caught {}".format(data.__class__))
        text = data.get("text")
        icon_url = data.get("icon_url") or None
        proxy_icon_url = data.get("proxy_icon_url") or None

        return cls(
            text=text,
            icon_url=icon_url,
            proxy_icon_url=proxy_icon_url
        )

    def toDict(self) -> Dict[str, str]:
        result = {
            "text": self.text
        }
        if self.icon_url:
            result["icon_url"] = self.icon_url
        if self.proxy_icon_url:
            result["proxy_icon_url"] = self.proxy_icon_url
        return result

    def __str__(self) -> str:
        return str(self.toDict())

    def __repr__(self) -> str:
        return ("Embed.Footer(text={},icon_url={},proxy_icon_url={})"
                .format(self.text, self.icon_url, self.proxy_icon_url))

class ImageObject(EmbedObject):
    """
    Represents image objects on discord Embed.
    Can be used at 'image', 'thumbnail' property (They share same options)
    """

    def __init__(
            self,
            url: str,
            proxy_url: Optional[str] = None,
            height: Optional[int] = None,
            width: Optional[int] = None
    ) -> None:
        if validate_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        if validate_url(proxy_url):
            self.proxy_url: Optional[str] = proxy_url
        else:
            self.proxy_url: Optional[str] = None

        self.height = height
        self.width = width

    @classmethod
    def fromDict(
        cls, 
        data: Dict[str, Any]
    ) -> ImageObject: # type: ignore
        # Type Check
        if not isinstance(data, dict):
            raise TypeError("Expected Dict[str, Any], caught {}".format(data.__class__))
        url = data.get("url")
        proxy_url = data.get("proxy_url") or None
        height = data.get("height") or None
        width = data.get("width") or None
        return cls(url, proxy_url, height, width)

    def toDict(self) -> Dict[str, str]:
        result = {
            "url": self.url
        }
        if self.proxy_url is not None:
            result["proxy_url"] = self.proxy_url
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        return result

    def __str__(self) -> str:
        return str(self.toDict())

    def __repr__(self) -> str:
        return ("Embed.Image(url={},proxy_url={},height={},width={}"
                .format(self.url, self.proxy_url, self.height, self.width))

ThumbnailObject = ImageObject


class VideoObject(EmbedObject):
    """
    Represents video objects on discord Embed.
    """

    def __init__(
        self, 
        url: str, 
        height: Optional[int] = None, 
        width: Optional[int] = None
    ):
        if validate_url(url):
            self.url = url
        else:
            raise ValueError("Invalid url!")

        self.height = height
        self.width = width

    @classmethod
    def fromDict(
        cls, 
        data: Dict[str, Any]
    ) -> VideoObject: # type: ignore
        # Type Check
        if not isinstance(data, dict):
            raise TypeError("Expected Dict[str, Any], caught {}".format(data.__class__))

        # Attribute Check
        url = data.get("url")
        height = data.get("height") or None
        width = data.get("width") or None
        return cls(
            url=url,
            height=height,
            width=width
        )

    def toDict(self) -> Dict[str, str]:
        result = {
            "url": self.url
        }
        if self.height is not None:
            result["height"] = self.height
        if self.width is not None:
            result["width"] = self.width
        return result

    def __str__(self) -> str:
        return str(self.toDict())

    def __repr__(self) -> str:
        return "Embed.Video(url={},height={},width={})".format(self.url, self.height, self.width)

class ProviderObject(EmbedObject):
    """
    Represents provider objects on discord Embed.
    """

    def __init__(
        self, 
        name: str, 
        url: str
    ) -> None:
        self.name = name
        self.url = url

    @classmethod
    def fromDict(
        cls, 
        data: Dict[str, Any]
    ) -> ProviderObject: # type: ignore
        # Type Check
        if not isinstance(data, dict):
            raise TypeError("Expected Dict[str, Any], caught {}".format(data.__class__))

        # Attribute Check
        try:
            name = data.get("name")
            url = data.get("url")
            return cls(
                name=name,
                url=url
            )

        except KeyError as e:
            raise ValueError(f"Invalid data is passed in VideoObject. : {data}. KeyError : {e}")

    def toDict(self) -> Dict[str, str]:
        result = {
            "name": self.name,
            "url": self.url
        }
        return result

    def __str__(self) -> str:
        return str(self.toDict())

    def __repr__(self) -> str:
        return "Embed.Provider(name={},url={})".format(self.name, self.url)

class Field(EmbedObject):
    """
    Represents field objects on discord Embed.
    """

    def __init__(
        self, 
        name: str, 
        value: str,
        inline: Optional[bool] = False
    ):

        if not Field.check_name(name):
            raise ValueError("")
        self.name = name
        if not Field.check_value(value):
            raise ValueError("")
        self.value = value
        if type(inline) != bool:
            inline = False
        self.inline = inline

    @classmethod
    def check_name(cls, name: str) -> bool:
        return type(name) is str and len(name) <= 256

    @classmethod
    def check_value(cls, value: str) -> bool:
        return type(value) is str and len(value) <= 1024

    @classmethod
    def fromDict(
        cls, 
        data: Union[Field, Dict[str, Union[str, bool]]] # type: ignore
    ) -> Optional[Field]: # type: ignore
        if isinstance(data, cls):
            return data
        if data is None or not isinstance(data, dict):
            raise TypeError("Expected Dict[str, Union[str, bool]], caught {}".format(data.__class__))
        try:
            name = data.get("name")
            if not cls.check_name(name):
                raise ValueError("")
            value = data.get("value")
            if not cls.check_value(value):
                raise ValueError("")
            inline = data.get("inline") or False
            if type(inline) != bool:
                raise TypeError("")
        # Does not except ValueError&TypeError, because it is intentionally raised to indicate error on given data.
        except KeyError as e:
            raise ValueError(f"Invalid data is passed in VideoObject. : {data}. KeyError : {e}")

    def toDict(self) -> Dict[str, str]:
        result = {
            "name": self.name,
            "value": self.value,
            "inline": self.inline
        }
        return result

    def __str__(self) -> str:
        return str(self.toDict())

    def __repr__(self) -> str:
        return ("Embed.Field(name={},value={},inline={})"
                .format(self.name, self.value, self.inline))

    def __getitem__(self, key) -> Optional[Any]:
        return getattr(self, key, None)

    def keys(self):
        def keyIter():
            yield "name"
            yield "value"
            yield "inline"
        return keyIter()

    def values(self):
        def valueIter():
            yield self.name
            yield self.value
            yield self.inline
        return valueIter()

    def items(self):
        def itemIter():
            yield "name", self.name
            yield "value", self.value
            yield "inline", self.inline
        return itemIter()

@NotImplemented
class Fields(EmbedObject, list):

    def __init__(self, fields: List[Field]):
        super().__init__()
        self.fields = []
        for field in fields:
            if not isinstance(field, Field):
                raise TypeError("field must be instance of Field object")
            self.fields.append(field)

    @classmethod
    def fromDict(cls, data: Dict[str, Any]) -> Fields: # type: ignore
        if isinstance(data, cls):
            return data
        if isinstance(data, list):
            return cls(data)

    def toDict(self) -> dict:
        return {
            "fields": str(self.fields)
        }

    def __getitem__(self, index: int) -> Field:
        return self.fields[index]

def check_title(value) -> bool:
    return type(value) == str and len(value) <= 256


def process_title(value: str) -> Union[str, NoReturn]:
    if check_title(value):
        return value

    raise ValueError("Embed title must be string object and its length must be lower than 256.")


def check_desc(value) -> bool:
    return type(value) == str and len(value) <= 2048


def process_desc(value: str) -> str:
    if check_desc(value):
        return value
    raise ValueError("Embed description must be string object and its length must be lower than 2048.")
