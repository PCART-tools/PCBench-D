import jax
import inspect

def main():
    backend = jax.lib.xla_bridge.get_backend()
    print("Backend:", backend.platform)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.lib.xla_bridge.get_backend))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()