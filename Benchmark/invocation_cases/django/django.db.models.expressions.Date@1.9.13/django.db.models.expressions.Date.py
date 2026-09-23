from django.conf import settings
import django
from django.db.models.expressions import Date
import inspect

settings.configure(USE_TZ=False)
django.setup()

def main():
    expr = Date("created_date", "year")
    print("Date expression object:", expr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Date))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()