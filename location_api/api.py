"""Publish stable APIs"""

from location_api import Point2D, Point3D, MCPosition, Location
from location_api.pos import get_player_pos

__version__ = "0.4.4"
VERSION = __version__
version = VERSION
"""The version string of LocationAPI plugin.
"""

__all__ = [
    "version",
    "Point2D",
    "Point3D",
    "MCPosition",
    "Location",
    "get_player_pos",
]
