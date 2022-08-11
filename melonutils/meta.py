import pkg_resources
from typing import NamedTuple, Literal

__all__ = (
    "__path__",
    "__author__",
    "__copyright__",
    "__license__",
    "__title__",
    "__version__",
    "version_info",
    "VersionInfo",
)

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int
    
version_info: VersionInfo = VersionInfo(major=0, minor=1, micro=0, releaselevel="alpha", serial=0)

__path__ = __import__("pkgutil").extend_path(__path__, __name__)
__author__ = 'Lemon Rose (japandotorg)'
__copyright__ = 'Copyright 2022 Lemon Rose (japandotorg) Melon-Development'
__license__ = 'MIT'
__title__ = 'melonutils'
__version__ = '.'.join(map(str, (version_info.major, version_info.minor, version_info.micro)))

pkg_resources.working_set.by_key.pop("melonutils", None)
