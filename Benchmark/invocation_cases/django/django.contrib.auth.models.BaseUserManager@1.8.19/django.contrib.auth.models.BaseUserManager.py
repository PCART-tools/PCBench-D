import inspect
from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    },
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    },
    MIDDLEWARE_CLASSES=(),
)

import django
django.setup()

from django.contrib.auth.models import BaseUserManager

def main():
    manager = BaseUserManager()
    #print(manager)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseUserManager))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
