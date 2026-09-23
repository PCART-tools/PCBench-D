import sympy as sp
import inspect
from sympy.core.trace import Tr
from sympy.matrices.expressions import MatrixSymbol

def main():
    A = MatrixSymbol('A', 2, 2)
    trace_expr = Tr(A)
    print("Trace expression:", trace_expr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Tr))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()