import jax
import jax.numpy as jnp
import inspect

def main():
    dtype = jnp.dtype('float32')
    result = jax.core.is_opaque_dtype(dtype)
    print("is_opaque_dtype result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.core.is_opaque_dtype))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()