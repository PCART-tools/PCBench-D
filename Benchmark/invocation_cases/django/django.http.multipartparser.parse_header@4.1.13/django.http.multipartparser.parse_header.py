import inspect
from django.http.multipartparser import parse_header

def main():
    header = b'text/plain; charset=utf-8'
    result = parse_header(header)
    print("parse_header result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(parse_header))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()