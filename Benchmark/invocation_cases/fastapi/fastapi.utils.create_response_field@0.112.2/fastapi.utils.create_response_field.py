from fastapi.utils import create_response_field
import inspect

def main():
    field_name = "example_field"
    field_type = str
    field_info = {}
    response_field = create_response_field(name=field_name, type_=field_type, field_info=field_info)
    print("create_response_field result:", response_field)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(create_response_field))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()