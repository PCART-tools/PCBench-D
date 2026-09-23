import os
import django
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
import inspect
import tempfile

def main():
    temp_dir = tempfile.mkdtemp()
    template_path = os.path.join(temp_dir, "hello.html")

    with open(template_path, "w", encoding="utf-8") as f:
        f.write("Hello, {{ name }}!")

    settings.configure(
        DEBUG=True,
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [temp_dir],
                'APP_DIRS': False,
            }
        ],
        INSTALLED_APPS=['django.contrib.contenttypes'],
    )

    django.setup()

    response = render_to_response(
        "hello.html",
        {"name": "World"}
    )

    print("render_to_response result:", response.content.decode())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(render_to_response))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()