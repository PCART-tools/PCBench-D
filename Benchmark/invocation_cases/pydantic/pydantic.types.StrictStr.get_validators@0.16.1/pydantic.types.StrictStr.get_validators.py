import inspect
from pydantic import BaseModel, StrictStr

class MyModel(BaseModel):
    name: StrictStr

def main():
    validators = StrictStr.get_validators()
    print("get_validators result:", list(validators))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(StrictStr.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()