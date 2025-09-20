# LocationAPI-MCDR

An API to define location or positon points.

## 描述

LocationAPI是一个用于定义Minecraft中位置点的API。它提供了Point2D、Point3D、MCPosition和Location类，可以方便地表示游戏中的坐标和位置信息。

## 安装

```bash
pip install -r requirements.txt
```

## 运行测试

### 使用unittest运行测试

```bash
python -m unittest tests.test_location_api
```

### 使用pytest运行测试（需要先安装测试依赖）

```bash
pip install pytest pytest-cov
pytest tests/
```

### 运行测试并生成覆盖率报告

```bash
pytest --cov=location_api tests/
```

## 类说明

- `Point2D`: 表示二维坐标点(x, z)
- `Point3D`: 表示三维坐标点(x, y, z)
- `MCPosition`: 表示Minecraft中的位置，包含一个Point3D和维度信息
- `Location`: 表示一个具体的位置，包含名称、描述和其他自定义属性

## 调试脚本

直接运行`location_api/__init__.py`可以进入交互式调试模式：

```bash
python location_api/__init__.py
```