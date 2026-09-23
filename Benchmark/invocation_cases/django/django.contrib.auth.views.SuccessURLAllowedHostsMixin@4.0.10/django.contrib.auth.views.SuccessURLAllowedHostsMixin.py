import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    ALLOWED_HOSTS=['example.com'],
    ROOT_URLCONF='django.contrib.auth.urls',
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
    ]
)

django.setup()

from django.contrib.auth.views import SuccessURLAllowedHostsMixin
import inspect

def main():
    mixin = SuccessURLAllowedHostsMixin()
    result = mixin.success_url_allowed_hosts
    print("SuccessURLAllowedHostsMixin result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SuccessURLAllowedHostsMixin))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
