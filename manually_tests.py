from unittest.mock import Mock, patch

# Mock ServerInterface.psi before importing location_api modules
mock_psi = Mock()

# Create a mock for ServerInterface class
with patch("mcdreforged.api.all.ServerInterface.psi", return_value=mock_psi):
    import location_api as lapi
    import location_api.pos as lpos


if __name__ == "__main__":
    # Existing test
    point1 = lapi.Point3D(x=1, y=2, z=3)
    point2 = lapi.Point3D(x=4, y=5, z=6)
    print(
        f"Distance between {point1} and {point2}: {point1.distance_to(point2)}"
    )

    # Test get_point3d_from_string
    print("\n=== Testing get_point3d_from_string ===")

    # Test 1: Normal case with 'd' suffix
    log1 = "CleMooling has the following entity data: [-524.5d, 71.0d, -66.5d]"
    result1 = lpos.get_point3d_from_string(log1)
    print("Test 1 - Normal with 'd' suffix:")
    print(f"  Input: {log1}")
    print(f"  Result: {result1}")
    assert result1 is not None
    assert abs(result1.x - (-524.5)) < 0.001
    assert abs(result1.y - 71.0) < 0.001
    assert abs(result1.z - (-66.5)) < 0.001

    # Test 2: Normal case without 'd' suffix
    log2 = "Some player: [-100, 200.5, 300.75]"
    result2 = lpos.get_point3d_from_string(log2)
    print("\nTest 2 - Without 'd' suffix:")
    print(f"  Input: {log2}")
    print(f"  Result: {result2}")
    assert result2 is not None
    assert abs(result2.x - (-100)) < 0.001
    assert abs(result2.y - 200.5) < 0.001
    assert abs(result2.z - 300.75) < 0.001

    # Test 3: With player name matching
    log3 = "CleMooling has the following entity data: [10.0d, 20.0d, 30.0d]"
    result3 = lpos.get_point3d_from_string(log3, player_name="CleMooling")
    print("\nTest 3 - Player name matching:")
    print(f"  Input: {log3}")
    print("  Player: CleMooling")
    print(f"  Result: {result3}")
    assert result3 is not None

    # Test 4: "No entity was found" returns None
    log4 = "No entity was found"
    result4 = lpos.get_point3d_from_string(log4)
    print("\nTest 4 - No entity case:")
    print(f"  Input: {log4}")
    print(f"  Result: {result4}")
    assert result4 is None

    # Test 5: Invalid format raises TypeError
    log5 = "Invalid log with no coordinates"
    print("\nTest 5 - Invalid format (should raise TypeError):")
    print(f"  Input: {log5}")
    try:
        result5 = lpos.get_point3d_from_string(log5)
        print(f"  ERROR: Expected TypeError but got {result5}")
    except TypeError as e:
        print(f"  Caught expected TypeError: {e}")

    # Test 6: Custom regex
    log6 = "Coords: (1.0, 2.0, 3.0)"
    custom_regex = (
        r"\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)"
    )
    result6 = lpos.get_point3d_from_string(log6, regex=custom_regex)
    print("\nTest 6 - Custom regex:")
    print(f"  Input: {log6}")
    print(f"  Regex: {custom_regex}")
    print(f"  Result: {result6}")
    assert result6 is not None
    assert abs(result6.x - 1.0) < 0.001
    assert abs(result6.y - 2.0) < 0.001
    assert abs(result6.z - 3.0) < 0.001

    # Test 7: Player name not found returns None
    log7 = (
        "DifferentPlayer has the following entity data: [10.0d, 20.0d, 30.0d]"
    )
    result7 = lpos.get_point3d_from_string(log7, player_name="CleMooling")
    print("\nTest 7 - Player name not found (should return None):")
    print(f"  Input: {log7}")
    print("  Player: CleMooling")
    print(f"  Result: {result7}")
    assert result7 is None

    print("\nAll tests passed!")
