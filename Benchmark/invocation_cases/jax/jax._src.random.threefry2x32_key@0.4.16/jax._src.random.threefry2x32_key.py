import jax
import jax.random as random
import inspect

def main():
    key = random.threefry2x32_key(0)
    print("threefry2x32_key result:", key)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(random.threefry2x32_key))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()