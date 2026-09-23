import django
from django.conf import settings
from django.apps import apps
from django.db import models
from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor
import inspect

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=['__main__'],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
django.setup()


class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

class FakeRel:
    pass


class FakeField:
    name = 'profile'
    null = False
    model = Author

    def __init__(self):
        self.rel = FakeRel()

    def get_cache_name(self):
        return '_profile_cache'

def main():
    field = FakeField()
    descriptor = ReverseSingleRelatedObjectDescriptor(field)

    print("Descriptor:", descriptor)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(type(descriptor)))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    apps.register_models(__name__, Author)
    main()