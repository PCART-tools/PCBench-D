import jax
import inspect
from jaxlib.xla_extension import OpSharding
from jax.sharding import OpShardingSharding

def main():
    devices = []  
    op_sharding = OpSharding()
    sharding = OpShardingSharding(devices, op_sharding)
    print("OpShardingSharding instance:", sharding)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(OpShardingSharding))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()