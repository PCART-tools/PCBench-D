import jax
import jax.numpy as jnp
from jax.interpreters.xla import device_put
import inspect

def main():
    # Create a JAX array
    arr = jnp.array([1, 2, 3, 4])
    # Use device_put to transfer the array to the device
    result = device_put(arr)
    print("device_put result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(device_put))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()