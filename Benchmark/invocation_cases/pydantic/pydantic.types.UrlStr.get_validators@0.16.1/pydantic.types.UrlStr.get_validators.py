import inspect
from pydantic import UrlStr

def main():
    validators = list(UrlStr.get_validators())
    print("get_validators result:", validators)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(UrlStr.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()