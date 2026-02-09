"""Location API for storing and manipulating Minecraft coordinates and locations.

This module provides a set of dataclasses to represent points in 2D and 3D space,
Minecraft positions (point + dimension), and named locations with metadata.
"""

from dataclasses import dataclass, fields
from typing import Self

from beartype import beartype
from primitive_type import (
    PrimitiveMap,
    get_primitive_object,
    is_nested_dict,
)


@dataclass
@beartype
class Point3D:
    """Define a 3D point with x, y, z coordinates.

    This class represents a point in 3D space with x, y, and z coordinates.
    It uses floating-point precision for coordinate values.
    """

    x: float
    """The x-coordinate of the point.
    """
    y: float
    """The y-coordinate of the point.
    """
    z: float
    """The z-coordinate of the point.
    """

    def __str__(self) -> str:
        return "[{}, {}, {}]".format(self.x, self.y, self.z)

    def distance_to(self, point: Self) -> float:
        """Calculate the Euclidean distance between this point and another point.

        :param point: The other 3D point to calculate the distance to.

        :return: The Euclidean distance between this point and another point.
        """
        return (
            (self.x - point.x) ** 2
            + (self.y - point.y) ** 2
            + (self.z - point.z) ** 2
        ) ** 0.5

    def distance2d_to(self, point: "Point3D | Point2D") -> float:
        """Calculate the 2D Euclidean distance between this point and another point.

        :param point: The other 2D or 3D point to calculate the distance to.

        :return: The 2D Euclidean distance between this point and another point.
        """
        return ((self.x - point.x) ** 2 + (self.z - point.z) ** 2) ** 0.5

    def height_to(self, point: Self) -> float:
        """Calculate the height difference between this point and another point.

        :param point: The other 3D point to calculate the height difference to.

        :return: The height difference between this point and another point.
        """
        return abs(self.y - point.y)

    @classmethod
    def from_point2d(cls, point: "Point2D", y: float) -> Self:
        """Create a 3D point from a 2D point and a height as y coordinate.

        :param point: The 2D point to create a 3D point from.
        :param y: The height of the 3D point.

        :return: The 3D point instance.
        """
        return cls(x=point.x, y=y, z=point.z)

    def to_point2d(self) -> "Point2D":
        """Create a 2D point from a 3D point.

        :return: The 2D point instance.
        """
        return Point2D(x=self.x, z=self.z)


@dataclass
@beartype
class Point2D:
    """Define a 2D point with x and z coordinates.

    This class represents a point in 2D space with x and z coordinates.
    It uses floating-point precision for coordinate values.
    """

    x: float
    """The x-coordinate of the point.
    """
    z: float
    """The z-coordinate of the point.
    """

    def __str__(self) -> str:
        return "[{}, {}]".format(self.x, self.z)

    def distance_to(self, point: Self) -> float:
        """Calculate the Euclidean distance between this point and another point.

        :param point: The other 2D point to calculate the distance to.

        :return: The Euclidean distance between this point and another point.
        """
        return ((self.x - point.x) ** 2 + (self.z - point.z) ** 2) ** 0.5

    def distance2d_to(self, point: "Point2D | Point3D") -> float:
        """Calculate the 2D Euclidean distance between this point and another point.

        :param point: The other 2D or 3D point to calculate the distance to.

        :return: The 2D Euclidean distance between this point and another point.
        """
        return ((self.x - point.x) ** 2 + (self.z - point.z) ** 2) ** 0.5

    @classmethod
    def from_point3d(cls, point: "Point3D") -> Self:
        """Create a 2D point from a 3D point.

        :param point: The 3D point to create a 2D point from.

        :return: The 2D point instance.
        """
        return cls(x=point.x, z=point.z)

    def to_point3d(self, y: float) -> "Point3D":
        """Create a 3d point from a 2d point and a height as y coordinate.

        :param y: The height of the 3d point.

        :return: The 3d point instance.
        """
        return Point3D(x=self.x, y=y, z=self.z)


@dataclass
class MCPosition:
    """Define a Minecraft position with a 3D point and a dimension.

    This class represents a position in Minecraft with a 3D point and a dimension.
    It uses floating-point precision for coordinate values.
    """

    point: "Point3D"
    """The 3D point of the position.
    """
    dimension: str  # e.g. minecraft:overworld
    """The dimension string of the position.
    """

    @property
    def x(self) -> float:
        """The x coordinate of the position."""
        return self.point.x

    @property
    def y(self) -> float:
        """The y coordinate of the position."""
        return self.point.y

    @property
    def z(self) -> float:
        """The z coordinate of the position."""
        return self.point.z

    def __str__(self) -> str:
        field_names = [f.name for f in fields(self)]
        values = [f"{_name}={getattr(self, _name)}" for _name in field_names]
        return f"{self.__class__.__name__}({', '.join(values)})"

    def asdict(self) -> dict:
        """Serialize :data:`MCPosition` object into a dict.

        :returns: The serialized dict.
        """
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "dimension": self.dimension,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Deserialize :data:`MCPosition` object from a dict.

        :param data: The dict to deserialize.
        :returns: The deserialized :data:`MCPosition` object.
        """
        dimension = get_primitive_object(
            data.get("dimension", data.get("dim", None)), str
        )
        assert isinstance(dimension, str)
        # check data
        for k, v in data.items():
            if ["x", "y", "z"] in k and "point" in k:
                raise TypeError("Invalid data: exists both coords and point!")
        point = data.get("point", None)
        if point:
            x = get_primitive_object(data.get("x"), float)
            assert isinstance(x, float)
            y = get_primitive_object(data.get("y"), float)
            assert isinstance(y, float)
            z = get_primitive_object(data.get("z"), float)
            assert isinstance(z, float)
        else:
            x = get_primitive_object(data.get("x"), float)
            assert isinstance(x, float)
            y = get_primitive_object(data.get("y"), float)
            assert isinstance(y, float)
            z = get_primitive_object(data.get("z"), float)
            assert isinstance(z, float)
        return cls(point=Point3D(x, y, z), dimension=dimension)


@dataclass
class Location:
    """Define a location with a name, description, and other fields.

    This class represents a location in Minecraft with a name, description, and other fields.
    It uses floating-point precision for coordinate values.
    """

    position: "MCPosition"
    """The position data of the location.
    """
    name: str
    """The name of the location.
    """
    description: str | None = None
    """The description of the location.
    """
    other: PrimitiveMap | None = None
    """Other informations about the location.
    """

    @property
    def x(self) -> float:
        """The x-coordinate of the location."""
        return self.position.x

    @property
    def y(self) -> float:
        """The y-coordinate of the location."""
        return self.position.y

    @property
    def z(self) -> float:
        """The z-coordinate of the location."""
        return self.position.z

    @property
    def dimension(self) -> str:
        """The dimension of the location."""
        return self.position.dimension

    def __post_init__(self):
        if self.other:
            if is_nested_dict(self.other):
                raise TypeError(
                    "Nested structures are not allowed in other field."
                )

    def __str__(self):
        field_names = [f.name for f in fields(self)]
        values = [f"{_name}={getattr(self, _name)}" for _name in field_names]
        return f"{self.__class__.__name__}({', '.join(values)})"

    def asdict(self) -> dict:
        """Serialize :data:`Location` object into a dict.

        :returns: The serialized dict.
        """
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "dimension": self.dimension,
            "name": self.name,
            "description": self.description,
            "other": self.other,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Deserialize :data:`Location` object from a dict.

        :param data: The dict to deserialize.
        :returns: The deserialized :data:`Location` object.
        """
        # check data
        for k, v in data.items():
            if ["x", "y", "z"] in k and "position" in k:
                raise TypeError(
                    "Invalid data: exists both coords and position!"
                )
        position = data.get("position", None)
        if position:
            position = MCPosition.from_dict(position)
            x = position.x
            y = position.y
            z = position.z
            dimension = position.dimension
        else:
            x = get_primitive_object(data.get("x"), float)
            y = get_primitive_object(data.get("y"), float)
            z = get_primitive_object(data.get("z"), float)
            assert isinstance(x, float)
            assert isinstance(y, float)
            assert isinstance(z, float)
            dimension = data.get("dimension", data.get("dim", None))
            if dimension:
                dimension = get_primitive_object(dimension)
                assert isinstance(dimension, str)
        name = get_primitive_object(data.get("name"), str)
        assert isinstance(name, str)
        description = data.get("description", data.get("desc", None))
        if description:
            description = get_primitive_object(description, str)
            assert isinstance(description, str)
        other = data.get("other", None)
        if other:
            if not is_nested_dict(other):
                raise TypeError(
                    "Nested structures are not allowed in other field."
                )
        return cls(
            MCPosition(Point3D(x, y, z), dimension), name, description, other
        )


# if __name__ == "__main__":
