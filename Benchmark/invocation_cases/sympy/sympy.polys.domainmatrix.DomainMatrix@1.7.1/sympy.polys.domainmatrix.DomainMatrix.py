import sympy
from sympy.polys.domainmatrix import DomainMatrix
import inspect

def main():
    matrix = DomainMatrix([[1, 2], [3, 4]], (2, 2), sympy.ZZ)
    print("DomainMatrix:", matrix)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(DomainMatrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()