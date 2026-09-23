import django
from django.contrib.postgres.fields import CITextField
import inspect


def main():
    field = CITextField()
    print("Field class:", type(field))
    print("Field internal type:", field.get_internal_type())
    print("Field deconstruction:", field.deconstruct())

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(CITextField))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()