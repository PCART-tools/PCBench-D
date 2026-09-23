import sympy
from sympy import FiniteSet,Set
import inspect

def main():
    set_a = FiniteSet(1, 2, 3)
    set_b = FiniteSet(1, 2, 3, 4, 5)
    result = Set.subset(set_a,set_b)
    print("subset result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Set.subset))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()