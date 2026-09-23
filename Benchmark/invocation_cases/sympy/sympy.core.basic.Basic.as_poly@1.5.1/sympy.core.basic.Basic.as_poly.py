import sympy as sp
import inspect

def main():
    x = sp.symbols('x')
    expr = x**2 + 2*x + 1
    poly = sp.Basic.as_poly(expr)
    print("as_poly result:", poly)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(sp.Basic.as_poly))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()