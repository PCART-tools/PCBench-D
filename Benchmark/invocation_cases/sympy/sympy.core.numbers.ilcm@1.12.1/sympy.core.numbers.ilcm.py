import sympy
import inspect

def main():
    result = sympy.ilcm(12, 18)
    print("ilcm result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sympy.ilcm))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()