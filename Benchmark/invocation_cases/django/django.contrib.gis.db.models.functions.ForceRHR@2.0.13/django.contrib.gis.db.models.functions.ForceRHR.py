import django
from django.conf import settings
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db.models.functions import ForceRHR
import inspect

settings.configure(DEBUG=True)

def main():
    # Create a polygon with counter-clockwise winding
    polygon = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)), srid=4326)

    # Apply ForceRHR using a common user-level calling pattern
    result = ForceRHR(polygon)
    print("ForceRHR result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ForceRHR))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
