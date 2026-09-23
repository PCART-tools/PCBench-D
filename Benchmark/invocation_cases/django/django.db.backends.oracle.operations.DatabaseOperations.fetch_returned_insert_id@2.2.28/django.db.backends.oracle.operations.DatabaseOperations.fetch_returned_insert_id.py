from django.conf import settings
import inspect

settings.configure(
    TIME_ZONE='UTC',
    USE_TZ=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': 'dummy',
            'USER': 'dummy',
            'PASSWORD': 'dummy',
        }
    }
)

import django
django.setup()

from django.db import connections
class FakeInsertIdVar:
    def getvalue(self):
        return [42]

class FakeCursor:
    def __init__(self):
        self._insert_id_var = FakeInsertIdVar()

def main():
    connection = connections['default']
    ops = connection.ops

    cursor = FakeCursor()

    insert_id = ops.fetch_returned_insert_id(cursor)
    print("fetch_returned_insert_id result:", insert_id)
    print("type:", type(insert_id))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ops.fetch_returned_insert_id))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
