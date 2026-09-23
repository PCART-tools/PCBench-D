import jax
import jax.numpy as jnp
import inspect

def main():
    data = {'a': jnp.array([1, 2, 3]), 'b': [4, 5]}
    tree_def = jax.tree_structure(data)
    print("tree_structure result:", tree_def)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.tree_structure))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()