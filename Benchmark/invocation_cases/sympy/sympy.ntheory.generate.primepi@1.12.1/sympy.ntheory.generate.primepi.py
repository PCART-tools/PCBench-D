import sympy
from sympy.ntheory import primepi
import inspect

def main():
    n = 10
    result = primepi(n)
    print("primepi result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(primepi))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()