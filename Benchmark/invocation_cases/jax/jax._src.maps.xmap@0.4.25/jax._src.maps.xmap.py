import jax
import jax.numpy as jnp
from jax.experimental.maps import xmap
import inspect

def main():
    def f(x):
        return x * 2

    x = jnp.array([1, 2, 3, 4])
    result = xmap(f, in_axes=['i'], out_axes=['i'])(x)
    print("xmap result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(xmap))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()