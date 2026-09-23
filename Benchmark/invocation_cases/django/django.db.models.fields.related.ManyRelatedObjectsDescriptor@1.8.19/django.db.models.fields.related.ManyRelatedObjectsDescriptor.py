import django
from django.conf import settings
from django.db import models
import inspect

settings.configure(
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
    class Meta:
        app_label = '__main__'


class Book(models.Model):
    authors = models.ManyToManyField(Author)

    class Meta:
        app_label = '__main__'


def main():
    from django.db.models.fields.related import ManyRelatedObjectsDescriptor
    m2m_field = Book._meta.get_field('authors')

    class FakeRelated(object):
        def __init__(self, field):
            self.field = field
            self.related_model = field.rel.to

    related = FakeRelated(m2m_field)
    descriptor = ManyRelatedObjectsDescriptor(related)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ManyRelatedObjectsDescriptor))
    except Exception as e:
        print(type(e).__name__,e)

if __name__ == "__main__":
    main()
