import sympy
from sympy.core.compatibility import ordered
import inspect

def main():
    data = {3, 1, 4, 2}
    result = list(ordered(data))
    print("ordered result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ordered))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()