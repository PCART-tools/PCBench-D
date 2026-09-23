import jax
from jax.interpreters.pxla import PartitionSpec
import inspect

def main():
    # Create a PartitionSpec instance
    partition_spec = PartitionSpec('x', 'y')
    print("PartitionSpec:", partition_spec)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(PartitionSpec))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()