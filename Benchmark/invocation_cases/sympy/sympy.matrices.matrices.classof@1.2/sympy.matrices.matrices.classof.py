import sympy
from sympy.matrices.matrices import classof
import inspect

def main():
    A = sympy.Matrix([[1, 2], [3, 4]])
    B = sympy.Matrix([[5, 6], [7, 8]])
    result = classof(A, B)
    print("classof result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(classof))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()