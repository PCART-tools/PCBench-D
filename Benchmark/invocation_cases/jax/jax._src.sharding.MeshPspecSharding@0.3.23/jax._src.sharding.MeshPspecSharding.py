import jax
import jax.numpy as jnp
from jax.experimental.maps import Mesh
from jax.experimental import PartitionSpec
from jax.sharding import MeshPspecSharding
import inspect

def main():
    # Create a device mesh
    devices = jax.devices()
    mesh = Mesh(devices, ('x',))
    
    # Create a PartitionSpec
    pspec = PartitionSpec('x')
    
    # Create a MeshPspecSharding object
    sharding = MeshPspecSharding(mesh, pspec)
    print("MeshPspecSharding result:", sharding)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(MeshPspecSharding))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()