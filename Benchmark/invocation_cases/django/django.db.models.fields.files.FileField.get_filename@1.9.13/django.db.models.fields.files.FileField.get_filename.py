import inspect
import django
from django.conf import settings
from django.db import models

# Ensure settings are configured
settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
)

django.setup()

def main():
    class TestModel(models.Model):
        file = models.FileField(upload_to='uploads/')

        class Meta:
            app_label = 'myapp'

    field = TestModel._meta.get_field("file")

    filename = field.get_filename("path/to/example.txt")

    print("get_filename result:", filename)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(field.get_filename))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()