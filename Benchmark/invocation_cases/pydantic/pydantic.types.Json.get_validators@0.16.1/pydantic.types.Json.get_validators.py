from pydantic import Json
import inspect

def main():
    validators = list(Json.get_validators())
    print("Validators:", validators)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Json.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()