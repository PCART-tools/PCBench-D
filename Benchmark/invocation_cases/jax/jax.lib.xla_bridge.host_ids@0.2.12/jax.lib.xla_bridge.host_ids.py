import jax
import inspect

def main():
    result = jax.lib.xla_bridge.host_ids()
    print("host_ids result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.lib.xla_bridge.host_ids))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()