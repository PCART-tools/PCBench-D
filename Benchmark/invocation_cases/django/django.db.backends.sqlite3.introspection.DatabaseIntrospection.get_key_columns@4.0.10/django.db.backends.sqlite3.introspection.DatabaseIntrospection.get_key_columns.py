import django
from django.conf import settings
from django.db import connections
from django.db.backends.sqlite3.introspection import DatabaseIntrospection
import inspect

def main():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
    )
    django.setup()

    connection = connections['default']
    with connection.cursor() as cursor:
        cursor.execute('CREATE TABLE example (id INTEGER PRIMARY KEY, name TEXT)')
        introspection = DatabaseIntrospection(connection)
        result = introspection.get_key_columns(cursor, 'example')
        print("get_key_columns result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DatabaseIntrospection.get_key_columns))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
