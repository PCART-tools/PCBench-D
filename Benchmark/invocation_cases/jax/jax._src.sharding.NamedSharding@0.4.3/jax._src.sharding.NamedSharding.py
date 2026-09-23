import numpy as np
import jax
from jax.experimental.pjit import NamedSharding
from jax.sharding import Mesh, PartitionSpec
import inspect

def main():
    devices = np.array(jax.devices())
    mesh = Mesh(devices, ('x',))
    sharding = NamedSharding(mesh, PartitionSpec('x'))
    print("NamedSharding:", sharding)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(NamedSharding))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()