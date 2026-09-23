@profiler.annotate_function
def shard_args(
    devices: Sequence[xb.xla_client.Device],
    indices: Sequence[Sequence[Index]],
    shardings: Sequence[sharding_internal.XLACompatibleSharding],
    args,
) -> Sequence[Sequence[xb.xla_client.Buffer]]:
  """Shard each argument data array along its leading axis.

  Args:
    devices: sequence of Devices mapping replica index to a physical device.
    indices: sequence of the same length as `args` describing how each arg
      should be sharded/replicated across `devices`. Each element in `indices`
      is the same length as `devices`.
    args: a sequence of JaxTypes representing arguments to be sharded according
      to `indices` and placed on `devices`.

  Returns:
    A list of length matching args, containing lists of per-device buffers
    for each argument.
  """
  return [shard_arg(arg, devices, indices[i], shardings[i])
          for i, arg in enumerate(args)]
