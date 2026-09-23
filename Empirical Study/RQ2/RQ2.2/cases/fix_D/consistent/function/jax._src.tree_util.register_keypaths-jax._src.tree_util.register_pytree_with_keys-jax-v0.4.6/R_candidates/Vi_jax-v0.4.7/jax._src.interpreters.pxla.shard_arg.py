def shard_arg(arg, devices, arg_indices, sharding):
  """Returns a list of size len(devices) containing per-device buffers.

  For the C++ pmap path, we fallback to Python (this function) to shard
  arguments that are not supported by the C++ `ShardArg`.

  Arrgs:
    arg: The Python argument.
    devices: The list of devices to shard over.
    arg_indices: A list of `len(devices)` indices to use to shard the argument.
  """
  arg = xla.canonicalize_dtype(arg)
  return shard_arg_handlers[type(arg)](arg, devices, arg_indices, sharding)
