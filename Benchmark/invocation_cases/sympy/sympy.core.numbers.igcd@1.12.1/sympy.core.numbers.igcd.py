import sympy
from sympy.core.numbers import igcd
import inspect

def main():
    a = 48
    b = 18
    result = igcd(a, b)
    print("igcd result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(igcd))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()