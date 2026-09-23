import inspect
from django.conf import settings
from django.forms.widgets import DateTimeInput

def main():
    settings.configure(USE_L10N=False, USE_TZ=True)
    
    widget = DateTimeInput(format='%Y-%m-%d %H:%M:%S')
    value = widget._format_value('2025-12-09 08:24:55')
    print("_format_value result:", value)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DateTimeInput._format_value))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()