import sympy
import inspect
from sympy.functions.combinatorial.numbers import carmichael

def main():
    start = 1
    end = 1000
    result = list(carmichael.find_carmichael_numbers_in_range(start, end))
    print("Carmichael numbers in range:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(carmichael.find_carmichael_numbers_in_range))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
