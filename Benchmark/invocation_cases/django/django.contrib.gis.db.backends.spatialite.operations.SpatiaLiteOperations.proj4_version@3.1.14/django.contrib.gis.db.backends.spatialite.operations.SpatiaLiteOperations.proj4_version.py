import inspect
from django.contrib.gis.db.backends.spatialite.operations import SpatiaLiteOperations

class FakeCursor:
    def __init__(self, value="FAKE_PROJ4 1.0"):
        self.value = value

    def execute(self, sql):
        pass

    def fetchone(self):
        return (self.value,)
    def close(self):
        pass


class FakeConnection:
    def _cursor(self):
        return FakeCursor()

def main():
    spatial_ops = SpatiaLiteOperations(connection=FakeConnection())
    result = spatial_ops.proj4_version()
    print("proj4_version result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SpatiaLiteOperations.proj4_version))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()