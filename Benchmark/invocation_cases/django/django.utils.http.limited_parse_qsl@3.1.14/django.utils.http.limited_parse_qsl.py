import inspect
from django.utils.http import limited_parse_qsl

def main():
    query_string = "a=1&b=2"

    result = limited_parse_qsl(query_string, fields_limit=2)
    print("limited_parse_qsl result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(limited_parse_qsl))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()