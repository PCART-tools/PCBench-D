from pydantic.types import ConstrainedInt
import inspect

def main():
    class MyInt(ConstrainedInt):
        gt = 0
        lt = 100

    validators = MyInt.get_validators()
    print("get_validators result:", list(validators))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(MyInt.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()