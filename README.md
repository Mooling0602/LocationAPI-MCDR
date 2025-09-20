# LocationAPI-MCDR

An API to define location or positon points.

## 描述

LocationAPI是一个用于定义Minecraft中位置点的API。它提供了Point2D、Point3D、MCPosition和Location类，可以方便地表示游戏中的坐标和位置信息。

LocationAPI同时也是ModernTeleport（现代化传送）插件的核心依赖。

测试内容如下：
```fish
(locationapi-mcdr) mooling@localhost /path/to/LocationAPI-MCDR (main)> .venv/bin/python location_api/__init__.py
Type coord x: 45
Type coord z: 456
Type coord y: 64
Type dimension: minecraft:the_end
Type location name: 小黑塔
Type location description: 末影人刷怪塔
Type other attributes by json string here: 
Location generating...
Location(position=MCPosition(point=x: 45.0, y: 64.0, z: 456.0, dimension=minecraft:the_end), name=小黑塔, description=末影人刷怪塔, other=None)
```