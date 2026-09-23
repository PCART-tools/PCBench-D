import inspect
from datetime import datetime
from django.conf import settings

settings.configure(
    TIME_ZONE='UTC',
    USE_TZ=True,
    USE_DEPRECATED_PYTZ=False,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.oracle',
            'NAME': 'dummy',  # 不会真的连接
            'USER': 'dummy',
            'PASSWORD': 'dummy',
        }
    }
)

import django
django.setup()

from django.db import connections

def main():
    connection = connections['default']
    ops = connection.ops
    value = datetime(2025, 12, 9, 12, 0, 0)
    tzname = 'UTC'
    result = ops._convert_field_to_tz(value, tzname)
    print("_convert_field_to_tz result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ops._convert_field_to_tz))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()