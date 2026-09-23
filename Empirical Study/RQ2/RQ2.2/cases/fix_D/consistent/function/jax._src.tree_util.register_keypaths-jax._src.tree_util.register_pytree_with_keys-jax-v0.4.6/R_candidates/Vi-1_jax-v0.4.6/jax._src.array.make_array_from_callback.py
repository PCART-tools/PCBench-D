def make_array_from_callback(
    shape: Shape, sharding: Sharding,
    data_callback: Callable[[Optional[Index]], ArrayLike]) -> ArrayImpl:
  """Returns a ``jax.Array`` via data fetched from ``data_callback``.

  ``data_callback`` is used to fetch the data for each addressable shard of the
  returned ``jax.Array``.

  Args:
    shape : Shape of the ``jax.Array``.
    sharding: A ``Sharding`` instance which describes how the ``jax.Array`` is
      laid out across devices.
    data_callback : Callback that takes indices into the global array value as
      input and returns the corresponding data of the global array value.
      The data can be returned as any array-like object, e.g. a ``numpy.ndarray``.

  Returns:
    A ``jax.Array`` via data fetched from ``data_callback``.

  Example:

    >>> import math
    >>> from jax.sharding import Mesh
    >>> from jax.sharding import PartitionSpec as P
    >>> import numpy as np
    ...
    >>> input_shape = (8, 8)
    >>> global_input_data = np.arange(math.prod(input_shape)).reshape(input_shape)
    >>> global_mesh = Mesh(np.array(jax.devices()).reshape(2, 4), ('x', 'y'))
    >>> inp_sharding = jax.sharding.NamedSharding(global_mesh, P('x', 'y'))
    ...
    >>> def cb(index):
    ...  return global_input_data[index]
    ...
    >>> arr = jax.make_array_from_callback(input_shape, inp_sharding, cb)
    >>> arr.addressable_data(0).shape
    (4, 2)
  """
  device_to_index_map = sharding.devices_indices_map(shape)
  # Use addressable_devices here instead of `_addressable_device_assignment`
  # because `_addressable_device_assignment` is only available on
  # `XLACompatibleSharding` and this function is supposed to work for every
  # `Sharding`.
  arrays = [
      api.device_put(data_callback(device_to_index_map[device]), device)
      for device in sharding.addressable_devices
  ]
  aval = core.ShapedArray(shape, arrays[0].dtype, weak_type=False)
  return ArrayImpl(aval, sharding, arrays, committed=True)
