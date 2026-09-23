import jax
import inspect

def main():
    # Test data
    dim = 5
    result = jax.core.non_negative_dim(dim)
    print("non_negative_dim result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.core.non_negative_dim))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()