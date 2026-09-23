import django
from django.conf import settings
import inspect

# Minimal Django setup for import compatibility
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

from django.contrib.postgres.fields.jsonb import KeyTextTransform

# Minimal instantiation to trigger import and usage
def main():
    transform = KeyTextTransform('key', 'data')
    print("KeyTextTransform instance created:", transform)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(KeyTextTransform))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()