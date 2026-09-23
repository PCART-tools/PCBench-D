import sympy
from sympy.combinatorics.fp_groups import _simplification_technique_1, FreeGroup
import inspect

def main():
    # Example input for the function
    F = FreeGroup("a b")
    a, b = F.generators
    rels = [a * b, b * a]
    result = _simplification_technique_1(rels)
    print("Simplification result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(_simplification_technique_1))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
