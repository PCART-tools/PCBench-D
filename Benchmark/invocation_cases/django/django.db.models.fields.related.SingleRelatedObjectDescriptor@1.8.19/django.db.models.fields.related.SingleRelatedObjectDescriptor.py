import django
from django.conf import settings
from django.db import models
from django.db.models.fields.related import SingleRelatedObjectDescriptor
import inspect

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[],
)
django.setup()

class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

class FakeRel:
    pass


class FakeField:
    name = 'author'
    model = Author
    null = False

    def __init__(self):
        self.rel = FakeRel()

    def get_cache_name(self):
        return '_author_cache'


def main():
    field = FakeField()
    descriptor = SingleRelatedObjectDescriptor(field)

    print("SingleRelatedObjectDescriptor:", descriptor)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(type(descriptor)))
    except Exception as e:
        print(type(e).__name__)


if __name__ == "__main__":
    main()