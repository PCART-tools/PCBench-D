import sympy as sp
import inspect

def main():
    n = 30
    result = sp.ntheory.reduced_totient(n)
    print("reduced_totient result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.ntheory.reduced_totient))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()