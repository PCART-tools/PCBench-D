import jax
import inspect

def main():
    # Simulate a trace context usage
    with jax.profiler.TraceContext("example_trace"):
        print("TraceContext is active")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.profiler.TraceContext))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()