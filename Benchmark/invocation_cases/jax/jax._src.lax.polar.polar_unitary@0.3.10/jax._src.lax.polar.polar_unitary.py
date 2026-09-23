import jax
import jax.numpy as jnp
from jax.scipy.linalg import polar_unitary
import inspect

def main():
    matrix = jnp.array([[1.0, 2.0], [3.0, 4.0]])
    unitary, _ = polar_unitary(matrix)
    print("polar_unitary result:", unitary)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(polar_unitary))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()