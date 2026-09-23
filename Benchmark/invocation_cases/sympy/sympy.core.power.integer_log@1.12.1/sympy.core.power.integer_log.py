import sympy as sp
import inspect

def main():
    base = 16
    n = 2
    result = sp.integer_log(base, n)
    print("integer_log result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.integer_log))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()