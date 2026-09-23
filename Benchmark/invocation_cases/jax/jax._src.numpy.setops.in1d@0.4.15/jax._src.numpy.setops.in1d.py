import jax.numpy as jnp
import inspect

def main():
    arr1 = jnp.array([1, 2, 3, 4])
    arr2 = jnp.array([2, 4, 6])
    result = jnp.in1d(arr1, arr2)
    print("in1d result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jnp.in1d))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()