import jax
import jax.numpy as jnp
from jax.interpreters.pxla import device_put
import inspect

def main():
    arr = jnp.array([1, 2, 3, 4])
    dev = jax.devices()[0]
    devices = [dev, dev, dev, dev]
    result = device_put(arr,devices)
    print("device_put result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(device_put))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()