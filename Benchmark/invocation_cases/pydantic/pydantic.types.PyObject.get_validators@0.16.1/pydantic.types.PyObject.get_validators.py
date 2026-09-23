import inspect
from pydantic.types import PyObject

def main():
    validators = list(PyObject.get_validators())
    print("get_validators result:", validators)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(PyObject.get_validators))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()