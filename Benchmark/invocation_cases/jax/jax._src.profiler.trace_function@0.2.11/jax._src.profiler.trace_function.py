import jax
import inspect

def main():
    def sample_function(x):
        return x * 2

    traced_function = jax.profiler.trace_function(sample_function)
    result = traced_function(5)
    print("trace_function result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.profiler.trace_function))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()