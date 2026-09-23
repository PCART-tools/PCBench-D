import django
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.apps import apps
import inspect

def main():
    settings.configure(
        DEBUG=True,
        STATIC_URL='/static/',
        INSTALLED_APPS=[
            'django.contrib.staticfiles',
        ]
    )
    apps.populate(settings.INSTALLED_APPS)
    
    file_path = 'example.css'
    result = static(file_path)
    print("static result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(static))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()