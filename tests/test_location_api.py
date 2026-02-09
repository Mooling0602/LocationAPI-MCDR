import unittest

from location_api import Location, MCPosition, Point2D, Point3D


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
        location = Location(
            position, "Test Location", "A test location", other_data
        )
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
            Location(
                position,
                "Test Location",
                "A test location",
                invalid_other_data,  # type: ignore
            )

    def test_location_string_representation(self):
        """测试Location类的字符串表示"""
        point3d = Point3D(1.0, 2.0, 3.0)
        position = MCPosition(point3d, "minecraft:overworld")
        other_data = {"key1": "value1", "key2": 123}
        location = Location(
            position, "Test Location", "A test location", other_data
        )

        location_str = str(location)
        self.assertIn("position=MCPosition", location_str)
        self.assertIn("name=Test Location", location_str)
        self.assertIn("description=A test location", location_str)
        self.assertIn("other={'key1': 'value1', 'key2': 123}", location_str)

    def test_coordinate_properties(self):
        """测试MCPosition和Location类的x, y, z自动推导属性"""
        point3d = Point3D(1.5, 2.5, 3.5)
        position = MCPosition(point3d, "minecraft:overworld")

        # 测试 MCPosition 的 x, y, z 属性
        self.assertEqual(position.x, 1.5)
        self.assertEqual(position.y, 2.5)
        self.assertEqual(position.z, 3.5)

        location = Location(position, "Test Location")

        # 测试 Location 的 x, y, z 属性
        self.assertEqual(location.x, 1.5)
        self.assertEqual(location.y, 2.5)
        self.assertEqual(location.z, 3.5)

    def test_mcposition_and_location_as_or_from_dict(self):
        """测试MCPosition和Location类的字典转换方法"""
        position = MCPosition(
            Point3D(12.3422, 64, 786.4633), "minecraft:overworld"
        )
        self.assertEqual(
            position.asdict(),
            {
                "x": 12.3422,
                "y": 64,
                "z": 786.4633,
                "dimension": "minecraft:overworld",
            },
        )

    def test_point3d_distance_to(self):
        """测试Point3D类的3D距离计算"""
        point1 = Point3D(0.0, 0.0, 0.0)
        point2 = Point3D(3.0, 4.0, 0.0)

        # 3-4-5三角形在XY平面，距离应该是5.0
        distance = point1.distance_to(point2)
        self.assertAlmostEqual(distance, 5.0, places=3)

    def test_point3d_distance2d_to_with_point3d(self):
        """测试Point3D类的2D距离计算（与另一个Point3D）"""
        point1 = Point3D(0.0, 10.0, 0.0)  # 高度不同
        point2 = Point3D(3.0, 20.0, 4.0)  # 高度不同

        # 2D距离应该忽略y坐标：sqrt(3² + 4²) = 5.0
        distance = point1.distance2d_to(point2)
        self.assertAlmostEqual(distance, 5.0, places=3)

    def test_point3d_distance2d_to_with_point2d(self):
        """测试Point3D类的2D距离计算（与Point2D）"""
        point3d = Point3D(0.0, 10.0, 0.0)
        point2d = Point2D(3.0, 4.0)

        distance = point3d.distance2d_to(point2d)
        self.assertAlmostEqual(distance, 5.0, places=3)

    def test_point3d_height_to(self):
        """测试Point3D类的高度差计算"""
        point1 = Point3D(0.0, 10.0, 0.0)
        point2 = Point3D(5.0, 25.0, 5.0)

        height_diff = point1.height_to(point2)
        self.assertAlmostEqual(height_diff, 15.0, places=3)

    def test_point3d_from_point2d(self):
        """测试从Point2D创建Point3D"""
        point2d = Point2D(1.0, 2.0)
        point3d = Point3D.from_point2d(point2d, y=3.0)

        self.assertEqual(point3d.x, 1.0)
        self.assertEqual(point3d.y, 3.0)
        self.assertEqual(point3d.z, 2.0)

    def test_point3d_to_point2d(self):
        """测试Point3D转换为Point2D"""
        point3d = Point3D(1.0, 2.0, 3.0)
        point2d = point3d.to_point2d()

        self.assertEqual(point2d.x, 1.0)
        self.assertEqual(point2d.z, 3.0)

    def test_point2d_distance_to(self):
        """测试Point2D类的距离计算"""
        point1 = Point2D(0.0, 0.0)
        point2 = Point2D(3.0, 4.0)

        distance = point1.distance_to(point2)
        self.assertAlmostEqual(distance, 5.0, places=3)

    def test_point2d_distance2d_to_with_point2d(self):
        """测试Point2D类的2D距离计算（与另一个Point2D）"""
        point1 = Point2D(0.0, 0.0)
        point2 = Point2D(3.0, 4.0)

        distance = point1.distance2d_to(point2)
        self.assertAlmostEqual(distance, 5.0, places=3)

    def test_point2d_distance2d_to_with_point3d(self):
        """测试Point2D类的2D距离计算（与Point3D）"""
        point2d = Point2D(0.0, 0.0)
        point3d = Point3D(3.0, 10.0, 4.0)  # 高度被忽略

        distance = point2d.distance2d_to(point3d)
        self.assertAlmostEqual(distance, 5.0, places=3)

    def test_point2d_to_point3d(self):
        """测试Point2D转换为Point3D"""
        point2d = Point2D(1.0, 2.0)
        point3d = point2d.to_point3d(y=3.0)

        self.assertEqual(point3d.x, 1.0)
        self.assertEqual(point3d.y, 3.0)
        self.assertEqual(point3d.z, 2.0)

    def test_point2d_from_point3d_already_tested(self):
        """测试Point2D.from_point3d方法（已存在但确保完整）"""
        point3d = Point3D(1.0, 2.0, 3.0)
        point2d = Point2D.from_point3d(point3d)

        self.assertEqual(point2d.x, 1.0)
        self.assertEqual(point2d.z, 3.0)


if __name__ == "__main__":
    unittest.main()
