#!/usr/bin/env python3
"""
测试运行脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import unittest
    
    # 发现并运行所有测试
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 如果有测试失败，返回非零退出码
    sys.exit(not result.wasSuccessful())