import location_api as lapi


if __name__ == "__main__":
    point1 = lapi.Point3D(x=1, y=2, z=3)
    point2 = lapi.Point3D(x=4, y=5, z=6)
    print(point1.distance_to(point2))
