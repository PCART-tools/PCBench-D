import jax
import inspect

def main():
    result = jax.lib.xla_bridge.host_count()
    print("host_count result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.lib.xla_bridge.host_count))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()