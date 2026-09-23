import jax
import jax.numpy as jnp
import inspect

def main():
    # Create a ShapedArray instance
    shape = (2, 3)
    dtype = jnp.float32
    array = jax.abstract_arrays.ShapedArray(shape, dtype)
    print("ShapedArray:", array)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.abstract_arrays.ShapedArray))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()