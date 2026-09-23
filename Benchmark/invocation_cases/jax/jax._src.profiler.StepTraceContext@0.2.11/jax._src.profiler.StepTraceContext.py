import jax
import inspect

def main():
    with jax.profiler.StepTraceContext("example_step"):
        print("StepTraceContext invoked")

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.profiler.StepTraceContext))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()