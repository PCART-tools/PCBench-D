import django
from django.conf import settings
from django.db import connections
import django.db.backends.mysql.operations as mysql_operations
from django.utils.timezone import utc
import datetime
import inspect

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dummy',
        }
    },
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

def main():
    connection = connections['default']
    operations = mysql_operations.DatabaseOperations(connection)

    field_sql = 'created_at'
    tzname = 'UTC'
    result = operations._convert_field_to_tz(field_sql, tzname)
    print("convert_datetimefield_value result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(mysql_operations.DatabaseOperations._convert_field_to_tz))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
