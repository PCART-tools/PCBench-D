import django
from django.conf import settings
from django.apps import apps
from django.contrib.postgres.fields import CIEmailField
from django.db import models
import inspect

# Configure Django settings
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.postgres',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

def main():
    # Initialize Django
    django.setup()

    # Define a model using CIEmailField
    class User(models.Model):
        email = CIEmailField()
        class Meta:
            app_label = 'test_app'

    # Create a User instance
    user = User(email='example@example.com')
    print("CIEmailField value:", user.email)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(CIEmailField))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()