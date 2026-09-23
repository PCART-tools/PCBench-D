import jax
from jax.experimental.maps import Mesh
import inspect

def main():
    devices = jax.devices()
    mesh = Mesh(devices, ('x',))
    print("Mesh:", mesh)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Mesh))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()