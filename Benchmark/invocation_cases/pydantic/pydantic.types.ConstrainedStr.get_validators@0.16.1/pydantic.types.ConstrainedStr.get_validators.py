from pydantic.types import ConstrainedStr
import inspect

def main():
    class MyStr(ConstrainedStr):
        gt = 0
        lt = 100

    validators = MyStr.get_validators()
    print("get_validators result:", list(validators))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(MyStr.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()