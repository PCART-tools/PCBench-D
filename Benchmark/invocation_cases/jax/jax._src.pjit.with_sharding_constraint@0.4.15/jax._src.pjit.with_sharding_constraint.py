import jax
import jax.numpy as jnp
from jax.experimental.pjit import with_sharding_constraint
from jax.sharding import PartitionSpec, Mesh, NamedSharding
import inspect

def main():
    x = jnp.array([1, 2, 3, 4])
    
    # Create a device mesh
    devices = jax.devices()
    mesh = Mesh(devices, ('x',))

    # Use NamedSharding
    named_sharding = NamedSharding(mesh, PartitionSpec('x'))
    result = with_sharding_constraint(x, named_sharding)
    print("with_sharding_constraint result:", result)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(with_sharding_constraint))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()