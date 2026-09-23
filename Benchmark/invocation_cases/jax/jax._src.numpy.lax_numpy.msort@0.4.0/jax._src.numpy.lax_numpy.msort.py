import jax.numpy as jnp
import inspect

def main():
    arr = jnp.array([[3, 2, 1], [6, 5, 4]])
    result = jnp.msort(arr)
    print("msort result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jnp.msort))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()