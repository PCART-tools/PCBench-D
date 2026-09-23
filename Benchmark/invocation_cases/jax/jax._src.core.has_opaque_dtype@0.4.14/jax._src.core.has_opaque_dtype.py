import jax
import jax.numpy as jnp
import inspect

def main():
    # Simulate input for the function
    example_input = jnp.ones((2, 2), dtype=jnp.float32)
    result = jax.core.has_opaque_dtype(example_input)
    print("has_opaque_dtype result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.core.has_opaque_dtype))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()