import sympy as sp
import inspect

def main():
    n = 6
    k = 1
    result = sp.divisor_sigma(n, k)
    print("divisor_sigma result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.divisor_sigma))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()