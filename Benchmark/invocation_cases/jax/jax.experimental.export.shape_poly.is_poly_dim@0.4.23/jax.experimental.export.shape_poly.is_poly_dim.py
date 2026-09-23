import jax
from jax.experimental.export.shape_poly import is_poly_dim
import inspect

def main():
    dim = "n"
    result = is_poly_dim(dim)
    print("is_poly_dim result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(is_poly_dim))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()