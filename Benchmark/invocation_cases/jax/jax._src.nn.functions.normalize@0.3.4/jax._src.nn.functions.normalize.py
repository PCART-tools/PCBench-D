import jax
import jax.numpy as jnp
import inspect

def main():
    x = jnp.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    result = jax.nn.normalize(x, axis=1)
    print("normalize result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.nn.normalize))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()