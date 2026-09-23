import django
from django.conf import settings
from django.db import connections
from django.db.backends.sqlite3.introspection import DatabaseIntrospection
import inspect

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()

def main():
    connection = connections['default']
    introspection = connection.introspection
    cursor = connection.cursor()
    result = DatabaseIntrospection.get_indexes(introspection, cursor, 'sqlite_master')
    print("get_indexes result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseIntrospection.get_indexes))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()