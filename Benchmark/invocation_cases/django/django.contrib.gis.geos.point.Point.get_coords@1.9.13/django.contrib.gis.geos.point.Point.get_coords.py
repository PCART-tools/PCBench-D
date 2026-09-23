import inspect
from django.contrib.gis.geos import Point

def main():
    point = Point(1, 2)
    coords = point.get_coords()
    print("get_coords result:", coords)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(point.get_coords))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()