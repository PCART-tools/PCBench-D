import sympy as sp
from sympy.stats import ContinuousRV, pspace
from sympy.stats.crv import ProductPSpace
from sympy import Interval, oo
import inspect

def main():
    x, y = sp.symbols('x y', positive=True)
    X = ContinuousRV(x, sp.exp(-x), Interval(0, oo))
    Y = ContinuousRV(y, sp.exp(-y), Interval(0, oo))
    PS = pspace((X, Y))
    result = ProductPSpace.integrate(PS,X,[X])
    print("integrate result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ProductPSpace.integrate))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()