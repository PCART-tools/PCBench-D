import django
from django.forms.widgets import Input
import inspect

def main():
    class CustomInput(Input):
        def __init__(self, attrs=None):
            super().__init__(attrs)

    widget = CustomInput()
    value = widget._format_value("test_value")
    print("_format_value result:", value)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Input._format_value))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()