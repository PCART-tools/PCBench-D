import os
import inspect
from django.conf import settings
from django.db import models
from django.core.wsgi import get_wsgi_application

def main():
    settings.configure(
        DEFAULT_INDEX_TABLESPACE='',
        INSTALLED_APPS=['__main__'],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
    )
    get_wsgi_application()

    class MyModel(models.Model):
        file = models.FileField(upload_to='uploads/')

        class Meta:
            app_label = '__main__'

    file_field = MyModel._meta.get_field('file')

    result = file_field.get_directory_name()
    print("get_directory_name result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(file_field.get_directory_name))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    main()