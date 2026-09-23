from sympy.functions.combinatorial.numbers import carmichael
import inspect

def main():
    n = 561
    result = carmichael.is_carmichael(n)
    print("is_carmichael result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(carmichael.is_carmichael))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()