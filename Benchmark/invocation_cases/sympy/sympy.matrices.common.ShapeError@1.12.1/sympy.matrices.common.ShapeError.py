import sympy
from sympy.matrices.common import ShapeError
import inspect

def main():
    try:
        raise ShapeError("test error")
    except ShapeError as e:
        print("Caught ShapeError:", e)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ShapeError))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()