import sympy as sp
from sympy.stats import ContinuousRV, density
from sympy.stats.crv import ConditionalContinuousDomain
import inspect

def main():
    x = sp.Symbol('x')
    pdf = sp.exp(-x)
    X = ContinuousRV(x, pdf, sp.Interval(0, sp.oo))
    domain = ConditionalContinuousDomain(X.pspace.domain, x > 1)
    
    result = domain.integrate(1)
    print("Integration result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(ConditionalContinuousDomain.integrate))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()