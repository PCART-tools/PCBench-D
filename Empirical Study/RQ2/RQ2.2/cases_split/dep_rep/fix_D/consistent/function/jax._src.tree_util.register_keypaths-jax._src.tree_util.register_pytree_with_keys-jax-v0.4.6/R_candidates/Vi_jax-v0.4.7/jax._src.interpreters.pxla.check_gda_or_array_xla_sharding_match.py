def check_gda_or_array_xla_sharding_match(
    args, in_xla_shardings: Sequence[sharding_impls.XLACompatibleSharding]) -> None:
  from jax._src.array import ArrayImpl

  for arg, xs in safe_zip(args, in_xla_shardings):
    if not isinstance(arg, ArrayImpl):
      continue

    # No need to cache this check since MeshExecutable has a C++ fast path
    # for AOT compiled call.
    if (not check_device_backend_on_shardings([xs]) and
        arg._committed and
        not are_op_shardings_equal(arg.sharding._to_xla_op_sharding(arg.ndim),
                                   xs._to_xla_op_sharding(arg.ndim))):
      raise ValueError(
          f"Array sharding does not match the input sharding. "
          f"Got Array sharding: {arg.sharding} and xla sharding: {xs} for "
          f"arg shape: {arg.shape}, arg value: {arg}")
