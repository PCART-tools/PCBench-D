import sympy
from sympy.matrices.matrices import a2idx
import inspect

def main():
    # Test data for a2idx
    index = 2
    size = 5
    result = a2idx(index, size)
    print("a2idx result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(a2idx))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()