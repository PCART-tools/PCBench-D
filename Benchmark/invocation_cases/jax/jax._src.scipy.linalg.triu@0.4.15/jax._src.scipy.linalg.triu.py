import jax
import jax.numpy as jnp
from jax.scipy.linalg import triu
import inspect

def main():
    matrix = jnp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    result = triu(matrix)
    print("triu result:\n", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(triu))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()