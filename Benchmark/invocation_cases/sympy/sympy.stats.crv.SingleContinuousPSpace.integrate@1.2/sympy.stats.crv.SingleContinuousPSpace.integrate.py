import sympy as sp
import inspect
from sympy.stats import ContinuousRV
from sympy.stats.crv import SingleContinuousPSpace
from sympy import Interval, oo

def main():
    x = sp.Symbol('x')
    pdf = sp.exp(-x)
    X = ContinuousRV(x, pdf, set=Interval(0, oo))
    space = X.pspace
    result = SingleContinuousPSpace.integrate(space,1, (x, 0, oo))
    print("integrate result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SingleContinuousPSpace.integrate))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
