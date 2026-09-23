import jax
import jax.random as random
import inspect
from jax import config
config.update("jax_enable_custom_prng", True)

def main():
    key = random.rbg_key(0)
    print("rbg_key result:", key)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(random.rbg_key))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()