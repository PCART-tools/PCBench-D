import inspect
import django
from django.conf import settings

# Minimal Django setup required for importing postgres fields
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.postgres',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        USE_I18N=True,
    )

django.setup()

from django.contrib.postgres.fields.jsonb import KeyTransform

def main():
    # Invoke KeyTransform in a minimal, user-level way
    kt = KeyTransform('key', 'data')
    print("KeyTransform instance created:", kt)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(KeyTransform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()