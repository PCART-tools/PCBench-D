from sympy import symbols, Interval, oo
from sympy.stats.crv import SingleContinuousDomain
import inspect

def main():
    x = symbols('x')
    domain = SingleContinuousDomain(x, Interval(-oo, oo))

    expr = x**2
    result = domain.integrate(expr)
    print("Integration result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(domain.integrate))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()