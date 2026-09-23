import jax
import jax.numpy as jnp
import inspect
from jax.interpreters.xla import abstractify

def main():
    x = jnp.array([1.0, 2.0, 3.0])
    result = abstractify(x)
    print("abstractify result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(abstractify))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()