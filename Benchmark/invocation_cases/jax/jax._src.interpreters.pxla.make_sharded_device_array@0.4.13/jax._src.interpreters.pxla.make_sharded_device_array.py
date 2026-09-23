import jax
import numpy as np
import inspect
from jax.interpreters import pxla
from jax.core import ShapedArray

def main():
    devices = jax.devices()
    aval = ShapedArray((3, 2), np.float32)

    arrays = [
        np.array([1., 1.], dtype=np.float32),
        np.array([2., 2.], dtype=np.float32),
        np.array([3., 3.], dtype=np.float32),
    ]

    device_buffers = [
        jax.device_put(x, d)
        for x, d in zip(arrays, devices[:3])
    ]

    sda = pxla.make_sharded_device_array(
        aval=aval,
        sharding_spec=None,
        device_buffers=device_buffers,
    )

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(pxla.make_sharded_device_array))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
