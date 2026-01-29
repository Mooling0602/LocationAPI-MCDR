from beartype import beartype
from dataclasses import dataclass, fields
from typing import Self

Primitive = str | int | float | bool | None
OtherField = dict[str, Primitive]


def is_primitive(val: object) -> bool:
    return isinstance(val, (str, int, float, bool)) or val is None


@dataclass
@beartype
class Point3D:
    x: float
    y: float
    z: float

    def __str__(self) -> str:
        return "[x: {}, y: {}, z: {}]".format(self.x, self.y, self.z)

    def distance_to(self, point: Self) -> float:
        return (
            (self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2
        ) ** 0.5

    def distance2d_to(self, point: Self | "Point2D") -> float:
        return ((self.x - point.x) ** 2 + (self.z - point.z) ** 2) ** 0.5

    def height_to(self, point: Self) -> float:
        return abs(self.y - point.y)

    @classmethod
    def from_point2d(cls, point: "Point2D", y: float) -> Self:
        return cls(x=point.x, y=y, z=point.z)

    def to_point2d(self) -> "Point2D":
        return Point2D(x=self.x, z=self.z)


@dataclass
@beartype
class Point2D:
    x: float
    z: float

    def __str__(self) -> str:
        return "[x: {}, z: {}]".format(self.x, self.z)

    def distance_to(self, point: Self) -> float:
        return ((self.x - point.x) ** 2 + (self.z - point.z) ** 2) ** 0.5

    def distance2d_to(self, point: Self | "Point3D") -> float:
        return ((self.x - point.x) ** 2 + (self.z - point.z) ** 2) ** 0.5

    @classmethod
    def from_point3d(cls, point: "Point3D") -> Self:
        return cls(x=point.x, z=point.z)

    def to_point3d(self, y: float) -> "Point3D":
        return Point3D(x=self.x, y=y, z=self.z)


@dataclass
class MCPosition:
    point: "Point3D"
    dimension: str  # e.g. minecraft:overworld

    def __str__(self):
        field_names = [f.name for f in fields(self)]
        values = [f"{_name}={getattr(self, _name)}" for _name in field_names]
        return f"{self.__class__.__name__}({', '.join(values)})"


@dataclass
class Location:
    position: "MCPosition"
    name: str
    description: str | None = None
    other: OtherField | None = None

    def __post_init__(self):
        if self.other:
            for k, v in self.other.items():
                if not is_primitive(v):
                    raise TypeError(
                        f"Invalid value for key '{k}': {v!r} (type {type(v).__name__}). "
                        f"Reason: Nested structures are not allowed."
                    )

    def __str__(self):
        field_names = [f.name for f in fields(self)]
        values = [f"{_name}={getattr(self, _name)}" for _name in field_names]
        return f"{self.__class__.__name__}({', '.join(values)})"
