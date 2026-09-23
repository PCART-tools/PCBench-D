import django
from django.conf import settings
from django.contrib.postgres.fields import JSONField
import inspect

settings.configure(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}})

def main():
    field = JSONField()
    print("JSONField instance:", field)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(JSONField))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()