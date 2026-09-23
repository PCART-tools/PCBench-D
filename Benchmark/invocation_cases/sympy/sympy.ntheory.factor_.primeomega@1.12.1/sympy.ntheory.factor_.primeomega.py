import sympy
import inspect

def main():
    number = 60
    result = sympy.primeomega(number)
    print("primeomega result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sympy.primeomega))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()