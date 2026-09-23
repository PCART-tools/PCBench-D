import inspect
from django.contrib.postgres.forms.jsonb import JSONString

def main():
    value = JSONString('{"key": "value"}')
    print("JSONString:", value)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(JSONString))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()