import inspect
from pydantic import BaseModel

def main():
    class ExampleModel(BaseModel):
        name: str
        age: int

    validators = ExampleModel.get_validators()
    print("get_validators result:", list(validators))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(BaseModel.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()