import jax
import jax.numpy as jnp
from jax.experimental.export import export
import inspect

def main():
    args = jnp.ones((2, 3), dtype=jnp.float32)
    polymorphic_shapes = None
    result = export.args_specs(args, polymorphic_shapes)
    print("args_specs result:", result)


    print("-----getsource_output-----")
    try:
        print(inspect.getsource(export.args_specs))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
