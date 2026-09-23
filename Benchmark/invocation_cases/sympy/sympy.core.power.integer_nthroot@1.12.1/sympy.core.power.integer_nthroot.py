import sympy
from sympy.core.power import integer_nthroot
import inspect

def main():
    # Test data
    number = 27
    n = 3
    result = integer_nthroot(number, n)
    print("integer_nthroot result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(integer_nthroot))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()