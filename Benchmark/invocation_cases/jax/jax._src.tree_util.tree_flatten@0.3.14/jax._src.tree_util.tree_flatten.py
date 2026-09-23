import jax
import inspect

def main():
    pytree = {'a': [1, 2, 3], 'b': (4, 5)}
    leaves, structure = jax.tree_flatten(pytree)
    print("tree_flatten result:", leaves, structure)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.tree_flatten))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()