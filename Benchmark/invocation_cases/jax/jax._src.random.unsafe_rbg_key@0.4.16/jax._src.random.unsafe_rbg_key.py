import jax
import jax.random as random
import inspect
from jax import config
config.update("jax_enable_custom_prng", True)


def main():
    seed = 42
    result = random.unsafe_rbg_key(seed)
    print("unsafe_rbg_key result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(random.unsafe_rbg_key))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()