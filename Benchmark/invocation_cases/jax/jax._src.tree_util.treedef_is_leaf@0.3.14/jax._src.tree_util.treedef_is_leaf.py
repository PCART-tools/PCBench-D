import jax
import inspect
from jax import tree_util

def main():
    treedef = tree_util.tree_structure([1, 2, [3, 4]])
    result = jax.treedef_is_leaf(treedef)
    print("treedef_is_leaf result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.treedef_is_leaf))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()