import sympy
from sympy.core.numbers import igcdex
import inspect

def main():
    a, b = 30, 50
    result = igcdex(a, b)
    print("igcdex result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(igcdex))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()