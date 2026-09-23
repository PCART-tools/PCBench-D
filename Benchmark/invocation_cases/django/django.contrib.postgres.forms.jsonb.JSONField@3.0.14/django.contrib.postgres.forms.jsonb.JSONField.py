import django
from django.conf import settings
from django import forms
from django.contrib.postgres.forms.jsonb import JSONField
from django.apps import apps
import inspect

settings.configure(
    USE_I18N=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',  # Required for certain Django functionalities
        'django.contrib.postgres',     # Required for JSONField
    ],
)

django.setup()

def main():
    class TestForm(forms.Form):
        data = JSONField()

    form = TestForm({'data': '{"key": "value"}'})
    print("is_valid:", form.is_valid())
    print("cleaned_data:", form.cleaned_data)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(JSONField))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()