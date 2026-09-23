import sympy as sp
from sympy.physics.mechanics import inertia, ReferenceFrame
import inspect

def main():
    N = ReferenceFrame('N')
    result = inertia(N, 1, 2, 3)
    print("inertia result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(inertia))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()