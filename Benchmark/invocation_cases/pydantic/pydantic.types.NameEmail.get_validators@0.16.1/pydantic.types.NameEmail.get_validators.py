from pydantic import NameEmail
import inspect

def main():
    validators = NameEmail.get_validators()
    print("get_validators result:", list(validators))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(NameEmail.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()