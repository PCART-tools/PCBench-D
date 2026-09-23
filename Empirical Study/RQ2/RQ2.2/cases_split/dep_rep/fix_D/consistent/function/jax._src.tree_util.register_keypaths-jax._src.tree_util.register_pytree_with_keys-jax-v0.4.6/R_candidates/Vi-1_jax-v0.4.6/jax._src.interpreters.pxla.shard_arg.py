def shard_arg(arg, devices, arg_indices, sharding):
  """Returns a list of size len(devices) containing per-device buffers.

  For the C++ pmap path, we fallback to Python (this function) to shard
  arguments that are not supported by the C++ `ShardArg`.

  Arrgs:
    arg: The Python argument.
    devices: The list of devices to shard over.
    arg_indices: A list of `len(devices)` indices to use to shard the argument.
  """
  if isinstance(arg, ShardedDeviceArray) and arg_indices == arg.indices:
    # The shard_arg_handlers allow an extensible set of types to be sharded, but
    # inline handling for ShardedDeviceArray as a special case for performance
    # NOTE: we compare indices instead of sharding_spec because
    # pmap_benchmark.pmapshard_args_benchmark indicates this is faster.
    return [
        buf if buf.device() == d else buf.copy_to_device(d)
        for d, buf in zip(devices, arg.device_buffers)
    ]
  else:
    arg = xla.canonicalize_dtype(arg)
    return shard_arg_handlers[type(arg)](arg, devices, arg_indices, sharding)
