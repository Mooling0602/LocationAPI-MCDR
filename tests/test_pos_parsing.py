"""location_api.pos模块中位置解析函数的测试"""
import unittest
from unittest.mock import Mock, patch

# Mock ServerInterface.psi before importing location_api modules
mock_psi = Mock()

# Create a mock for ServerInterface class
with patch("mcdreforged.api.all.ServerInterface.psi", return_value=mock_psi):
    from location_api.pos import (
        get_point3d_from_server_reply,
        get_dimension_from_server_reply,
    )


class TestPositionParsing(unittest.TestCase):
    """位置解析函数的测试用例"""

    def test_get_point3d_from_server_reply_normal_with_d_suffix(self):
        """测试正常情况，带有'd'后缀"""
        log = "CleMooling has the following entity data: [-524.5d, 71.0d, -66.5d]"
        result = get_point3d_from_server_reply(log)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.x, -524.5, places=3)
        self.assertAlmostEqual(result.y, 71.0, places=3)
        self.assertAlmostEqual(result.z, -66.5, places=3)

    def test_get_point3d_from_server_reply_without_d_suffix(self):
        """测试正常情况，不带'd'后缀"""
        log = "Some player: [-100, 200.5, 300.75]"
        result = get_point3d_from_server_reply(log)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.x, -100, places=3)
        self.assertAlmostEqual(result.y, 200.5, places=3)
        self.assertAlmostEqual(result.z, 300.75, places=3)

    def test_get_point3d_from_server_reply_player_name_matching(self):
        """测试玩家名称匹配的情况"""
        log = "CleMooling has the following entity data: [10.0d, 20.0d, 30.0d]"
        result = get_point3d_from_server_reply(log, player_name="CleMooling")
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.x, 10.0, places=3)
        self.assertAlmostEqual(result.y, 20.0, places=3)
        self.assertAlmostEqual(result.z, 30.0, places=3)

    def test_get_point3d_from_server_reply_no_entity_found(self):
        """测试'No entity was found'返回None的情况"""
        log = "No entity was found"
        result = get_point3d_from_server_reply(log)
        
        self.assertIsNone(result)

    def test_get_point3d_from_server_reply_invalid_format_raises_typeerror(self):
        """测试无效格式引发TypeError的情况"""
        log = "Invalid log with no coordinates"
        
        with self.assertRaises(TypeError) as context:
            get_point3d_from_server_reply(log)
        
        self.assertIn("Could not extract 3D point", str(context.exception))

    def test_get_point3d_from_server_reply_custom_regex(self):
        """测试使用自定义正则表达式模式的情况"""
        log = "Coords: (1.0, 2.0, 3.0)"
        custom_regex = r"\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)"
        result = get_point3d_from_server_reply(log, regex=custom_regex)
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.x, 1.0, places=3)
        self.assertAlmostEqual(result.y, 2.0, places=3)
        self.assertAlmostEqual(result.z, 3.0, places=3)

    def test_get_point3d_from_server_reply_player_name_not_found(self):
        """测试提供了玩家名称但在内容中未找到的情况"""
        log = "DifferentPlayer has the following entity data: [10.0d, 20.0d, 30.0d]"
        result = get_point3d_from_server_reply(log, player_name="CleMooling")
        
        self.assertIsNone(result)

    def test_get_point3d_from_server_reply_invalid_number_format(self):
        """测试匹配的值无法转换为float的情况"""
        # 使用自定义正则表达式来匹配非数字字符串
        # 这样正则表达式能匹配，但float()转换会失败
        log = "Invalid: [abc, def, ghi]"
        custom_regex = r"\[(\w+),\s*(\w+),\s*(\w+)\]"
        
        with self.assertRaises(TypeError) as context:
            get_point3d_from_server_reply(log, regex=custom_regex)
        
        self.assertIn("Could not convert matched values to float", str(context.exception))

    def test_get_dimension_from_server_reply_normal_case(self):
        """测试维度提取的正常情况"""
        log = "CleMooling has the following entity data: minecraft:overworld"
        result = get_dimension_from_server_reply(log)
        
        self.assertEqual(result, "overworld")

    def test_get_dimension_from_server_reply_with_player_name(self):
        """测试维度提取，带有玩家名称匹配"""
        log = "CleMooling has the following entity data: minecraft:nether"
        result = get_dimension_from_server_reply(log, player="CleMooling")
        
        self.assertEqual(result, "nether")

    def test_get_dimension_from_server_reply_player_not_found(self):
        """测试维度提取，当玩家名称未找到时"""
        log = "DifferentPlayer has the following entity data: minecraft:overworld"
        result = get_dimension_from_server_reply(log, player="CleMooling")
        
        self.assertIsNone(result)

    def test_get_dimension_from_server_reply_no_match(self):
        """测试维度提取，当未找到维度信息时"""
        log = "No dimension information here"
        result = get_dimension_from_server_reply(log)
        
        self.assertIsNone(result)

    def test_get_dimension_from_server_reply_custom_regex(self):
        """测试维度提取，使用自定义正则表达式"""
        log = "Dimension: custom_dimension"
        custom_regex = r"Dimension:\s*(\w+)"
        result = get_dimension_from_server_reply(log, regex=custom_regex)
        
        self.assertEqual(result, "custom_dimension")


if __name__ == "__main__":
    unittest.main()