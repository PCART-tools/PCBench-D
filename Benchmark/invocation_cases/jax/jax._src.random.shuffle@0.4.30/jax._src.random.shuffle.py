import jax
import jax.numpy as jnp
import jax.random as random
import inspect

def main():
    key = random.PRNGKey(0)
    arr = jnp.array([1, 2, 3, 4, 5])
    shuffled_arr = random.shuffle(key, arr)
    print("shuffled array:", shuffled_arr)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(random.shuffle))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()