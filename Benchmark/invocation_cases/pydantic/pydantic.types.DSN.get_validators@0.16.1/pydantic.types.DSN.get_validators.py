import inspect
from pydantic.types import DSN

def main():
    validators = DSN.get_validators()
    print("get_validators result:", list(validators))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DSN.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()