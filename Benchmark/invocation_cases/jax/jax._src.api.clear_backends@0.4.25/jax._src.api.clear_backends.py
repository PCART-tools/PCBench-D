import jax
import inspect

def main():
    result = jax.clear_backends()
    print("clear_backends result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.clear_backends))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()