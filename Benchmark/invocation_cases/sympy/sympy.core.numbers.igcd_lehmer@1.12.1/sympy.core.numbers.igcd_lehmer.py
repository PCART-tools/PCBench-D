import sympy
from sympy.core.numbers import igcd_lehmer
import inspect

def main():
    a, b = 1071, 462
    result = igcd_lehmer(a, b)
    print("igcd_lehmer result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(igcd_lehmer))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()