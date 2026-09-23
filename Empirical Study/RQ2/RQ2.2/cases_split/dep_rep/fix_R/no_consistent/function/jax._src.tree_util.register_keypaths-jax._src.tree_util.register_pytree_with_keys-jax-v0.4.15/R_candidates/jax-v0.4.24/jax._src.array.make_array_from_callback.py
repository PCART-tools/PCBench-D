def make_array_from_callback(
    shape: Shape, sharding: Sharding,
    data_callback: Callable[[Index | None], ArrayLike]) -> ArrayImpl:
  """Returns a ``jax.Array`` via data fetched from ``data_callback``.

  ``data_callback`` is used to fetch the data for each addressable shard of the
  returned ``jax.Array``. This function must return concrete arrays, meaning that
  ``make_array_from_callback`` has limited compatibility with JAX transformations
  like :func:`jit` or :func:`vmap`.

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
  has_device_assignment = False
  if sharding.is_fully_replicated:
    if isinstance(sharding, XLACompatibleSharding):
      devices = list(sharding._addressable_device_assignment)
      has_device_assignment = True
    else:
      devices = list(sharding.addressable_devices)
    per_device_values = [data_callback((slice(None),) * len(shape))] * len(devices)
  else:
    device_to_index_map = sharding.addressable_devices_indices_map(shape)
    devices = list(device_to_index_map.keys())
    per_device_values = [data_callback(device_to_index_map[device])
                         for device in devices]

  if isinstance(per_device_values[0], core.Tracer):
    raise errors.UnexpectedTracerError(
        "jax.make_array_from_callback cannot be called within a traced context.")

  first_value = xla.canonicalize_dtype(per_device_values[0])
  aval = core.ShapedArray(shape, first_value.dtype, weak_type=False)

  # TODO(yashkatariya): Look into taking this path for non-fully replicated
  # shardings too.
  if (sharding.is_fully_replicated and has_device_assignment and
      not dtypes.issubdtype(aval.dtype, dtypes.extended)):
    # Do this check outside because `batched_device_put` won't do these checks
    # like ArrayImpl. This is a fast path for fully replicated arrays with
    # xla compatible sharding.
    if shape != first_value.shape:
      raise ValueError(
            f"Expected shard shape {shape} doesn't match the single device "
            f"array shape {first_value.shape}. Shape of Array is "
            f"{aval.str_short()} with sharding {sharding}")
    return pxla.batched_device_put(
        aval, sharding, per_device_values, devices, committed=True)

  arrays = api.device_put(per_device_values, devices)
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    return aval.dtype._rules.make_sharded_array(aval, sharding, arrays,
                                                committed=True)
  return ArrayImpl(aval, sharding, arrays, committed=True)
