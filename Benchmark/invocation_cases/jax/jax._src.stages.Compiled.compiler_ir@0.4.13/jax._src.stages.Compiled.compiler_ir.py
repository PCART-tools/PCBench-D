import jax
import jax.numpy as jnp
import inspect

def main():
    # Define a simple function to compile
    def simple_function(x):
        return jnp.sin(x) + jnp.cos(x)

    jit_fn = jax.jit(simple_function)
    lowered = jit_fn.lower(jnp.array(1.0))
    compiled = lowered.compile()
    print(type(compiled))
    compiler_ir_result = compiled.compiler_ir()
    print("compiler_ir result:", compiler_ir_result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(compiled.compiler_ir))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()