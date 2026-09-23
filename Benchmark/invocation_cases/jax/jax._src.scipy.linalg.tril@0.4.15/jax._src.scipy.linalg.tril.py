import jax
import jax.numpy as jnp
import inspect

def main():
    matrix = jnp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = jax.scipy.linalg.tril(matrix)
    print("tril result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.scipy.linalg.tril))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()