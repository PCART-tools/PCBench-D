from sympy.stats import FiniteRV
from sympy import symbols
from sympy.stats.frv import FinitePSpace
import inspect

def main():
    X = FiniteRV('X', {0: 0.2, 1: 0.3, 2: 0.5})
    pspace = X.pspace
    result = FinitePSpace.integrate(pspace,X)

    print(result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(FinitePSpace.integrate))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()