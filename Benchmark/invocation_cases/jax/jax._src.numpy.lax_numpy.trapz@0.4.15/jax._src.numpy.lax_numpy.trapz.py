import jax.numpy as jnp
import inspect

def main():
    y = jnp.array([1, 2, 3])
    x = jnp.array([0, 1, 2])
    result = jnp.trapz(y, x)
    print("trapz result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jnp.trapz))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()