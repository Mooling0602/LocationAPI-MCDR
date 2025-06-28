from dataclasses import dataclass
from typing import Optional, Self, Union

Primitive = Union[str, int, float, bool, None]
OtherField = dict[str, Primitive]


def is_primitive(val: object) -> bool:
    return isinstance(val, (str, int, float, bool)) or val is None


@dataclass
class Point3D:
    x: float
    y: float
    z: float

    def __str__(self) -> str:
        return "[{}, {}, {}]".format(self.x, self.y, self.z)


@dataclass
class Point2D:
    x: float
    z: float

    def __str__(self) -> str:
        return "[{}, {}]".format(self.x, self.z)

    @classmethod
    def from_point3d(cls, point: Point3D) -> Self:
        return cls(x=point.x, z=point.z)


@dataclass
class MCPosition:
    point: Point3D
    dimension: str  # example: minecraft:overworld

    def __str__(self):
        fields = ", ".join(f"{k}={getattr(self, k)}" for k in self.__dataclass_fields__)
        return f"{self.__class__.__name__}({fields})"


@dataclass
class Location:
    position: MCPosition
    name: str
    description: Optional[str] = None
    other: Optional[OtherField] = None

    def __post_init__(self):
        if self.other:
            for k, v in self.other.items():
                if not is_primitive(v):
                    raise TypeError(
                        f"Invalid value for key '{k}': {v!r} (type {type(v).__name__}). \nReason: Nested structures are not allowed."
                    )

    def __str__(self):
        fields = ", ".join(f"{k}={getattr(self, k)}" for k in self.__dataclass_fields__)
        return f"{self.__class__.__name__}({fields})"


if __name__ == "__main__":
    try:
        x = input("Type coord x: ")
        if x == "":
            print("Coordinate imcomplete, exiting...")
            exit()
        else:
            x = float(x)
        z = input("Type coord z: ")
        if z == "":
            print("Coordinate imcomplete, exiting...")
            exit()
        else:
            z = float(z)
        point_2d = Point2D(x, z)
        y = input("Type coord y: ")
        if y == "":
            print("Point2D generating...")
            print(point_2d)
            exit()
        else:
            y = float(y)
        point_3d = Point3D(x, y, z)
        dimension = input("Type dimension: ")
        if dimension == "":
            print("Point3D generating...")
            print(point_3d)
            exit()
        name = input("Type location name: ")
        if name == "":
            print("MCPosition generating...")
            print(MCPosition(point_3d, dimension))
            exit()
        description = input("Type location description: ")
        if description == "":
            description = None
        import json

        other = input("Type other attributes by json string here: ")
        if other == "":
            other = None
        else:
            try:
                other = json.loads(other)
                if not isinstance(other, dict):
                    other = None
            except json.decoder.JSONDecodeError:
                other = None
        print("Location generating...")
        print(Location(MCPosition(point_3d, dimension), name, description, other))
    except KeyboardInterrupt:  # Press Ctrl+C then Enter.
        print("Exiting script debug mode...")
    except EOFError:  # Press Ctrl+D
        print("\nExiting script debug mode...")
