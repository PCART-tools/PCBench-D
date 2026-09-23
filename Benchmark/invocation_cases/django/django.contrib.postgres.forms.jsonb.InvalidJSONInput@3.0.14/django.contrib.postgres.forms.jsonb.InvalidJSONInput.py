import inspect
from django.contrib.postgres.forms.jsonb import InvalidJSONInput

def main():
    # Create an instance of InvalidJSONInput
    invalid_json = InvalidJSONInput("Invalid JSON data")
    print("InvalidJSONInput instance:", invalid_json)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(InvalidJSONInput))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()