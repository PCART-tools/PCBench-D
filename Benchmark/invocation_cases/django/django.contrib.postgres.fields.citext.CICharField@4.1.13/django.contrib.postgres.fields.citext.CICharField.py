import inspect
from django.contrib.postgres.fields import CICharField
from django.db import models
import os
import django
from django.conf import settings

# Setting up a minimal Django environment
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.postgres',
        '__main__',  # Add the current module as an installed app
    ]
)
django.setup()

# Simulating a Django model using CICharField
class TestModel(models.Model):
    name = CICharField(max_length=100)

    class Meta:
        app_label = '__main__'  # Declare an explicit app label

def main():
    # Output the field's class name to confirm usage
    field = TestModel._meta.get_field('name')
    print("Field class:", field.__class__.__name__)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(CICharField))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()