import jax
import jax.numpy as jnp
import inspect

def main():
    arr = jnp.array([1, 2, 3])
    dev = arr.device()
    print("device:", dev)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(type(arr).device))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()