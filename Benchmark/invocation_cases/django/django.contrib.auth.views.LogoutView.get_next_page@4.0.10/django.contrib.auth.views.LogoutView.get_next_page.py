import django
from django.conf import settings

settings.configure(
    DEBUG=True,
    SECRET_KEY='fake-key',
    ALLOWED_HOSTS=['*'],
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
    ],
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        },
    ],
)

django.setup()

from django.contrib.auth.views import LogoutView
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
import inspect

def apply_middlewares(request):
    def get_response(req):
        return None

    for mw in (SessionMiddleware, AuthenticationMiddleware, MessageMiddleware):
        mw(get_response).process_request(request)

def main():
    factory = RequestFactory()
    request = factory.get('/logout/')

    request.user = type(
        'User',
        (),
        {
            'is_authenticated': True,
            'is_anonymous': False,
        }
    )()

    apply_middlewares(request)

    view = LogoutView()
    view.request = request
    view.args = ()
    view.kwargs = {}

    result = view.get_next_page()
    print("get_next_page result:", result)

    print("-----getsource_output-----")
    print(inspect.getsource(LogoutView.get_next_page))

if __name__ == "__main__":
    main()
