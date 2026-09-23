import django
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.core.wsgi import get_wsgi_application
import inspect

def main():
    settings.configure(
        USE_I18N=True,
        USE_L10N=True,
        USE_TZ=True,
        SECRET_KEY='fake-key',
        ROOT_URLCONF=__name__,
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.admin',
            'django.contrib.gis',
            '__main__',
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ],
    )

    django.setup()
    application = get_wsgi_application()

    from django.contrib.gis.admin import GeoModelAdmin

    class MyModel(models.Model):
        name = models.CharField(max_length=50)

        class Meta:
            app_label = '__main__'

    class MyGeoModelAdmin(GeoModelAdmin):
        pass

    admin_site = admin.sites.AdminSite()
    admin_instance = MyGeoModelAdmin(MyModel, admin_site)
    print("GeoModelAdmin instance created:", admin_instance)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(GeoModelAdmin))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
