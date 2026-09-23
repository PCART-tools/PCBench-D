import sympy
from sympy.core.power import isqrt
import inspect

def main():
    number = 16
    result = isqrt(number)
    print("isqrt result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(isqrt))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()