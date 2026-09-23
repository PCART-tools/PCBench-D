import jax
import inspect

def main():
    # Create a mock sharding object
    sharding = jax.sharding.XLACompatibleSharding()
    print("XLACompatibleSharding instance:", sharding)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(jax.sharding.XLACompatibleSharding))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()