import sympy
from sympy.utilities.iterables import postorder_traversal
import inspect

def main():
    expr = sympy.sympify('x + y*(z + 1)')
    result = list(postorder_traversal(expr))
    print("postorder_traversal result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(postorder_traversal))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()