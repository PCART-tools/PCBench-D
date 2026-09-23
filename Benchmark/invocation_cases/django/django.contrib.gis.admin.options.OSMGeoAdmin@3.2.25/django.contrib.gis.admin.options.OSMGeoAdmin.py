import inspect
import django
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.core.wsgi import get_wsgi_application

def main():
    if not settings.configured:
        settings.configure(
            USE_I18N=True,
            LANGUAGE_CODE='en-us',
            SECRET_KEY='dummy',
            ROOT_URLCONF=__name__,
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'django.contrib.admin',
                'django.contrib.gis',
                '__main__',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            MIDDLEWARE=[],
            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                },
            ]
        )

    django.setup()
    get_wsgi_application()

    from django.contrib.gis.admin.options import OSMGeoAdmin

    class MyModel(models.Model):
        name = models.CharField(max_length=100)

        class Meta:
            app_label = '__main__'

    class MyOSMGeoAdmin(OSMGeoAdmin):
        pass

    admin_site = admin.sites.AdminSite()
    admin_instance = MyOSMGeoAdmin(MyModel, admin_site)
    print("OSMGeoAdmin instance created:", admin_instance)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(OSMGeoAdmin))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
