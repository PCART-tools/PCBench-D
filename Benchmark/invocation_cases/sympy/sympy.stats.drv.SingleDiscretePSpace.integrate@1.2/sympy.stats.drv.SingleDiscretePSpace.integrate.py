from sympy.stats import Poisson
from sympy import symbols
from sympy.stats.drv import SingleDiscretePSpace
import inspect

def main():
    X = Poisson('X', 2)
    pspace = X.pspace
    k = symbols('k', integer=True, nonnegative=True)

    result = SingleDiscretePSpace.integrate(pspace,k)
    print(result)
    print("-----getsource_output-----")
    try:
        print(inspect.getsource(SingleDiscretePSpace.integrate))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()