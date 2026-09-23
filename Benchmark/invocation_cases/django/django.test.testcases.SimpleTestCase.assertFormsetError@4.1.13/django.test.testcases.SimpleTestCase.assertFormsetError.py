import inspect
from django import forms
from django.conf import settings
from django.test import SimpleTestCase
from django.apps import apps

# Configure settings
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',  # Required for form rendering
    ],
    FORM_RENDERER='django.forms.renderers.DjangoTemplates'
)

apps.populate(settings.INSTALLED_APPS)

class SampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()

class TestFormsetError(SimpleTestCase):
    def test_assert_formset_error(self):
        SampleFormSet = forms.formset_factory(SampleForm, extra=1)
        formset = SampleFormSet(data={
            'form-0-name': '',
            'form-0-age': 'invalid',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0'
        })
        
        formset.is_valid()
        
        self.assertFormsetError(formset, form_index=0, field='age', errors='Enter a whole number.')

def main():
    test_case = TestFormsetError()
    test_case.test_assert_formset_error()
    print("assertFormsetError executed successfully.")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(TestFormsetError.assertFormsetError))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()