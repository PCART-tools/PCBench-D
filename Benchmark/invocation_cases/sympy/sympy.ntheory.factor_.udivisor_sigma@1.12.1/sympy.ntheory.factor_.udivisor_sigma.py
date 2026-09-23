import sympy as sp
import inspect

def main():
    n = 6
    k = 2
    result = sp.ntheory.factor_.udivisor_sigma(n, k)
    print("udivisor_sigma result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.ntheory.factor_.udivisor_sigma))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()