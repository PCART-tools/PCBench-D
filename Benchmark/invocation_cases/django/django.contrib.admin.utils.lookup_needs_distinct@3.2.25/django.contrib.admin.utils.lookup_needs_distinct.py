import django
from django.conf import settings
from django.db import models
from django.contrib.admin.utils import lookup_needs_distinct
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin import ModelAdmin
from django.contrib import admin
from django.apps import apps
import inspect

# Minimal Django settings
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.admin',
        '__main__',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    MIDDLEWARE=[],
    ROOT_URLCONF=__name__,
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

django.setup()

class ExampleModel(models.Model):
    example_field = models.CharField(max_length=100)

    class Meta:
        app_label = '__main__'

class ExampleModelAdmin(ModelAdmin):
    list_display = ('example_field',)

def main():
    model = ExampleModel
    admin_site = admin.sites.AdminSite()
    model_admin = ExampleModelAdmin(model, admin_site)
    queryset = model.objects.all()
    opts = model._meta
    result = lookup_needs_distinct(opts, 'example_field')
    print("lookup_needs_distinct result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(lookup_needs_distinct))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
