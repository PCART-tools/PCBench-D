import sympy as sp
from sympy.algebras.quaternion import Quaternion
import inspect

def main():
    q = Quaternion(1, 2, 3, 4)
    result = q._ln()
    print("_ln result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Quaternion._ln))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()