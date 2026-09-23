import jax
import inspect

def main():
    # Create a ShapedArray instance
    shape = (2, 3)
    dtype = jax.numpy.float32
    shaped_array = jax.ShapedArray(shape, dtype)
    print("ShapedArray:", shaped_array)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.ShapedArray))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()