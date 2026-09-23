import sympy as sp
import inspect

def main():
    n = 10
    result = sp.mobius(n)
    print("mobius result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.mobius))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()