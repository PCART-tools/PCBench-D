from pydantic.types import ConstrainedFloat
import inspect

def main():
    class MyFloat(ConstrainedFloat):
        gt = 0
        lt = 100

    validators = MyFloat.get_validators()
    print("get_validators result:", list(validators))

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(MyFloat.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()