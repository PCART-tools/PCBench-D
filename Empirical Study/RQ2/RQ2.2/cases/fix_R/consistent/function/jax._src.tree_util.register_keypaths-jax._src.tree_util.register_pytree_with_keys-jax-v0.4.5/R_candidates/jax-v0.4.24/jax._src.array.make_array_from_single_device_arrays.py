def make_array_from_single_device_arrays(
    shape: Shape, sharding: Sharding, arrays: Sequence[basearray.Array]
) -> ArrayImpl:
  r"""Returns a ``jax.Array`` from a sequence of ``jax.Array``\s each on a single device.
      Every device in input ``sharding``\'s mesh must have an array in ``arrays``\s.

  Args:
    shape : Shape of the output ``jax.Array``. This conveys information already included with
      ``sharding`` and ``arrays`` and serves as a double check.
    sharding: Sharding: A global Sharding instance which describes how the output jax.Array is laid out across devices.
    arrays: Sequence of ``jax.Array``\s that are each single device addressable. ``len(arrays)``
      must equal ``len(sharding.addressable_devices)`` and the shape of each array must be the same. For multiprocess code,
      each process will call with a different ``arrays`` argument that corresponds to that processes' data.
      These arrays are commonly created via ``jax.device_put``.

  Returns:
    A global ``jax.Array``, sharded as ``sharding``, with shape equal to ``shape``, and with per-device
      contents matching ``arrays``.

  Examples:

    In this single-process example, we use ``make_array_from_single_device_arrays`` to create an
    a global array.

    >>> import math
    >>> from jax.sharding import Mesh
    >>> from jax.sharding import PartitionSpec as P
    >>> import numpy as np
    ...
    >>> mesh_rows = 2
    >>> mesh_cols =  jax.device_count() // 2
    ...
    >>> global_shape = (8, 8)
    >>> mesh = Mesh(np.array(jax.devices()).reshape(mesh_rows, mesh_cols), ('x', 'y'))
    >>> sharding = jax.sharding.NamedSharding(mesh, P('x', 'y'))
    >>> inp_data = np.arange(math.prod(global_shape)).reshape(global_shape)
    ...
    >>> arrays = [
    ...    jax.device_put(inp_data[index], d)
    ...        for d, index in sharding.addressable_devices_indices_map(global_shape).items()]
    ...
    >>> arr = jax.make_array_from_single_device_arrays(global_shape, sharding, arrays)
    >>> assert arr.shape == (8,8) # arr.shape is (8,8) regardless of jax.device_count()

    When using multiple processes, a common data pipeling is to have data parallelism across devices,
    with each device receiving at least one example. In this case, the following recipe will use
    `make_array_from_single_device_arrays` to create a global jax.Array.

    First, we create the per host data as Numpy arrays.

    >>> sharding = jax.sharding.NamedSharding(mesh, P(('x', 'y'),))
    >>> rows_per_device = 2
    >>> feature_length = 32
    >>> per_device_shape = (rows_per_device, feature_length)
    >>> per_host_shape = (rows_per_device * len(mesh.local_devices), feature_length)
    >>> per_host_generator = lambda : np.arange(np.prod(per_host_shape)).reshape(per_host_shape)
    >>> per_host_data = per_host_generator() # replace with your own per-host data pipeline that outputs numpy arrays

    Second, we put the Numpy data onto the local devices as single device Jax Arrays. Then we call
    make_array_from_single_device_arrays to make the global Array.

    >>> global_shape = (rows_per_device * len(sharding.device_set), ) + per_device_shape[1:]
    >>> per_device_data = np.split(per_host_data, len(mesh.local_devices), axis = 0) # per device data, but on host
    >>> per_device_data_on_device = jax.device_put(per_device_data, mesh.local_devices) # per device data, now on device
    >>> output_global_array = jax.make_array_from_single_device_arrays(global_shape, sharding, per_device_data_on_device)
    ...
    >>> assert output_global_array.addressable_data(0).shape == per_device_shape
    >>> assert output_global_array.shape == global_shape

    When using tensor parallelism (equivalent to sharding across both rows and columns in the
    above example), the above example doesn't generate the data in the sharding that you plan
    to consume it with. The most common fix is to simply load the data in this data parallel sharding
    and have the reshard happen automatically within the downstream jitted function.
    Depending on your use case, you might prefer to directly load sharded data, something that
    ``make_array_from_single_device_arrays`` can do but will depend on your data loading pipeline
    also loading in the matching sharding. Loading in a data parallel format is typically
    fully satisfactory for data loading for LLM use cases.

  """
  # All input arrays should be committed. Checking it is expensive on
  # single-controller systems.
  if any(isinstance(arr, core.Tracer) for arr in arrays):
    raise ValueError("jax.make_array_from_single_device_arrays requires a list of concrete arrays as input. "
                     f"got types {set(map(type, arrays))}")
  aval = core.ShapedArray(shape, arrays[0].dtype, weak_type=False)
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    return aval.dtype._rules.make_sharded_array(aval, sharding, arrays, committed=True)
  # TODO(phawkins): ideally the cast() could be checked.
  return ArrayImpl(aval, sharding, cast(Sequence[ArrayImpl], arrays),
                   committed=True)
