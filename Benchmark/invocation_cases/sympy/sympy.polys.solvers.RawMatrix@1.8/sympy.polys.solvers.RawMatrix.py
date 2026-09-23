import sympy
from sympy.polys.solvers import RawMatrix
import inspect

def main():
    # Create a RawMatrix instance
    matrix = RawMatrix([[1, 2], [3, 4]])
    print("RawMatrix result:", matrix)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(RawMatrix))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()