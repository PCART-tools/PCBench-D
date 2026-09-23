import jax
import inspect
from jax.abstract_arrays import raise_to_shaped
from jax.core import ShapedArray

def main():
    shaped_array = ShapedArray((2, 2), jax.numpy.float32)
    result = raise_to_shaped(shaped_array)
    print("raise_to_shaped result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(raise_to_shaped))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()