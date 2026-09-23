import inspect
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ],
    MIGRATION_MODULES={
        'auth': None,  
    },
)

import django
django.setup()

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

def main():
    class CustomUser(AbstractBaseUser):
        email = models.EmailField(unique=True)
        USERNAME_FIELD = 'email'

        class Meta:
            app_label = 'testapp'

    user_instance = CustomUser(
        email="test@example.com",
        password="password123"
    )
    print("AbstractBaseUser instance created:", user_instance)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(AbstractBaseUser))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
