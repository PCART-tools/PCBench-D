def make_array_from_single_device_arrays(
    shape: Shape, sharding: Sharding, arrays: Sequence[basearray.Array]
) -> ArrayImpl:
  r"""Returns a ``jax.Array`` from a sequence of ``jax.Array``\s on a single device.

  ``jax.Array`` on a single device is analogous to a ``DeviceArray``. You can use
  this function if you have already ``jax.device_put`` the value on a single
  device and want to create a global Array. The smaller ``jax.Array``\s should be
  addressable and belong to the current process.

  Args:
    shape : Shape of the ``jax.Array``.
    sharding: A ``Sharding`` instance which describes how the ``jax.Array`` is
      laid out across devices.
    arrays: Sequence of ``jax.Array``\s that are on a single device.

  Returns:
    A ``jax.Array`` from a sequence of ``jax.Array``\s on a single device.

  Example:

    >>> import math
    >>> from jax.sharding import Mesh
    >>> from jax.sharding import PartitionSpec as P
    >>> import numpy as np
    ...
    >>> global_shape = (8, 8)
    >>> global_mesh = Mesh(np.array(jax.devices()).reshape(2, 4), ('x', 'y'))
    >>> sharding = jax.sharding.NamedSharding(global_mesh, P('x', 'y'))
    >>> inp_data = np.arange(math.prod(global_shape)).reshape(global_shape)
    ...
    >>> arrays = [
    ...     jax.device_put(inp_data[index], d)
    ...     for d, index in sharding.addressable_devices_indices_map(global_shape).items()]
    ...
    >>> arr = jax.make_array_from_single_device_arrays(global_shape, sharding, arrays)
    >>> arr.addressable_data(0).shape
    (4, 2)

    In multi-process case, if the input is process local and data parallel
    i.e. each process receives a different part of the data, then you can use
    `make_array_from_single_device_arrays` to create a global jax.Array

    >>> local_shape = (8, 2)
    >>> global_shape = (jax.process_count() * local_shape[0], ) + local_shape[1:]
    >>> local_array = np.arange(math.prod(local_shape)).reshape(local_shape)
    >>> arrays = jax.device_put(
    ...   np.split(local_array, len(global_mesh.local_devices), axis = 0), global_mesh.local_devices)
    >>> sharding = jax.sharding.NamedSharding(global_mesh, P(('x', 'y'), ))
    >>> arr = jax.make_array_from_single_device_arrays(global_shape, sharding, arrays)
    >>> arr.addressable_data(0).shape
    (1, 2)
  """
  # All input arrays should be committed. Checking it is expensive on
  # single-controller systems.
  aval = core.ShapedArray(shape, arrays[0].dtype, weak_type=False)
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    return aval.dtype._rules.make_sharded_array(aval, sharding, arrays, committed=True)
  # TODO(phawkins): ideally the cast() could be checked. Revisit this after
  # removing DeviceArray.
  return ArrayImpl(aval, sharding, cast(Sequence[ArrayImpl], arrays),
                   committed=True)
