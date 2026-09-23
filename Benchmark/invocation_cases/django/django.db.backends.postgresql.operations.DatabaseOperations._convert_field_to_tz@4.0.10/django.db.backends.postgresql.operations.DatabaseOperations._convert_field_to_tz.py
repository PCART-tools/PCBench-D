import django
from django.conf import settings
from django.db import connection
from django.db.backends.postgresql.operations import DatabaseOperations
import inspect

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'test_db',
            'USER': 'test_user',
            'PASSWORD': 'test_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
)

def main():
    operations = DatabaseOperations(connection)
    field = 'timestamp_field'
    tzname = 'UTC'
    result = operations._convert_field_to_tz(field, tzname)
    print("_convert_field_to_tz result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseOperations._convert_field_to_tz))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()