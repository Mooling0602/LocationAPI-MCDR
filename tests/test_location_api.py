import unittest

from location_api import Point2D, Point3D, MCPosition, Location


class TestLocationAPI(unittest.TestCase):
    def test_point2d_creation(self):
        """测试Point2D类的创建和字符串表示"""
        point = Point2D(1.0, 2.0)
        self.assertEqual(point.x, 1.0)
        self.assertEqual(point.z, 2.0)
        self.assertEqual(str(point), "[1.0, 2.0]")

    def test_point3d_creation(self):
        """测试Point3D类的创建和字符串表示"""
        point = Point3D(1.0, 2.0, 3.0)
        self.assertEqual(point.x, 1.0)
        self.assertEqual(point.y, 2.0)
        self.assertEqual(point.z, 3.0)
        self.assertEqual(str(point), "[1.0, 2.0, 3.0]")

    def test_point2d_from_point3d(self):
        """测试Point2D从Point3D创建的功能"""
        point3d = Point3D(1.0, 2.0, 3.0)
        point2d = Point2D.from_point3d(point3d)
        self.assertEqual(point2d.x, 1.0)
        self.assertEqual(point2d.z, 3.0)

    # noinspection SpellCheckingInspection
    def test_mcposition_creation(self):
        """测试MCPosition类的创建和字符串表示"""
        point3d = Point3D(1.0, 2.0, 3.0)
        position = MCPosition(point3d, "minecraft:overworld")
        self.assertEqual(position.point, point3d)
        self.assertEqual(position.dimension, "minecraft:overworld")
        # 测试字符串表示包含所有字段
        position_str = str(position)
        self.assertIn("point=[1.0, 2.0, 3.0]", position_str)
        self.assertIn("dimension=minecraft:overworld", position_str)

    def test_location_creation_without_optional_fields(self):
        """测试Location类（不带可选字段）的创建和字符串表示"""
        point3d = Point3D(1.0, 2.0, 3.0)
        position = MCPosition(point3d, "minecraft:overworld")
        location = Location(position, "Test Location")
        self.assertEqual(location.position, position)
        self.assertEqual(location.name, "Test Location")
        self.assertIsNone(location.description)
        self.assertIsNone(location.other)

    def test_location_creation_with_optional_fields(self):
        """测试Location类（带可选字段）的创建和字符串表示"""
        point3d = Point3D(1.0, 2.0, 3.0)
        position = MCPosition(point3d, "minecraft:overworld")
        other_data = {"key1": "value1", "key2": 123}
        location = Location(position, "Test Location", "A test location", other_data)
        self.assertEqual(location.position, position)
        self.assertEqual(location.name, "Test Location")
        self.assertEqual(location.description, "A test location")
        self.assertEqual(location.other, other_data)

    def test_location_with_invalid_other_field(self):
        """测试Location类在other字段包含嵌套结构时抛出异常"""
        point3d = Point3D(1.0, 2.0, 3.0)
        position = MCPosition(point3d, "minecraft:overworld")
        invalid_other_data = {"key": {"nested": "value"}}

        with self.assertRaises(TypeError):
            Location(position, "Test Location", "A test location", invalid_other_data)

    def test_location_string_representation(self):
        """测试Location类的字符串表示"""
        point3d = Point3D(1.0, 2.0, 3.0)
        position = MCPosition(point3d, "minecraft:overworld")
        other_data = {"key1": "value1", "key2": 123}
        location = Location(position, "Test Location", "A test location", other_data)

        location_str = str(location)
        self.assertIn("position=MCPosition", location_str)
        self.assertIn("name=Test Location", location_str)
        self.assertIn("description=A test location", location_str)
        self.assertIn("other={'key1': 'value1', 'key2': 123}", location_str)


if __name__ == "__main__":
    unittest.main()
