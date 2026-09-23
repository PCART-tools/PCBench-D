def check_gda_or_array_xla_sharding_match(
    args, in_xla_shardings: Sequence[sharding_internal.XLACompatibleSharding]) -> None:
  from jax._src.global_device_array import GlobalDeviceArray
  from jax._src.array import ArrayImpl

  for arg, xs in safe_zip(args, in_xla_shardings):
    if not isinstance(arg, (GlobalDeviceArray, ArrayImpl)):
      continue
    if isinstance(arg, GlobalDeviceArray):
      arg_sharding = create_mesh_pspec_sharding(arg.mesh, arg.mesh_axes)
      arg_type = 'GDA'
      committed = True
    else:
      arg_sharding = arg.sharding
      arg_type = 'Array'
      committed = arg._committed

    # No need to cache this check since MeshExecutable has a C++ fast path
    # for AOT compiled call.
    if (not check_device_backend_on_shardings([xs]) and
        committed and
        not are_op_shardings_equal(arg_sharding._to_xla_op_sharding(arg.ndim),
                                   xs._to_xla_op_sharding(arg.ndim))):
      raise ValueError(
          f"{arg_type} sharding does not match the input sharding. "
          f"Got {arg_type} sharding: {arg_sharding} and xla sharding: {xs} for "
          f"arg shape: {arg.shape}, arg value: {arg}")
