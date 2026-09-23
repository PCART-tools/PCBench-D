import sympy as sp
import inspect

def main():
    a = 3
    m = 11
    result = sp.mod_inverse(a, m)
    print("mod_inverse result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.mod_inverse))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()