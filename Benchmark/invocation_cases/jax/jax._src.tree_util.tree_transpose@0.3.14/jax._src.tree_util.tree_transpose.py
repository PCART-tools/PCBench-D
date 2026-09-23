import jax
import jax.tree_util as tu
import inspect

def main():
    # Transposed layout: outer list is axis_tree structure
    pytree = [
        {'a': 1, 'b': 2},
        {'a': 3, 'b': 4}
    ]
    axis_tree = [0, 1]

    result = jax.tree_transpose(
        tu.tree_structure(axis_tree),
        tu.tree_structure(pytree[0]),
        pytree
    )
    print("tree_transpose result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.tree_transpose))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
