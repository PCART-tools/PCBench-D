import jax
import inspect

def main():
    pytree = {'a': [1, 2], 'b': {'c': 3, 'd': 4}}
    result = jax.tree_leaves(pytree)
    print("tree_leaves result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.tree_leaves))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()