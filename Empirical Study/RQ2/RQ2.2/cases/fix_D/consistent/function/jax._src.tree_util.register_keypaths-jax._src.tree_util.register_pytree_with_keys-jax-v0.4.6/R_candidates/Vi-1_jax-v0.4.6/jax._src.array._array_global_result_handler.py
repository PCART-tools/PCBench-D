def _array_global_result_handler(global_aval, out_sharding, committed,
                                 is_out_sharding_from_xla):
  if global_aval.dtype == dtypes.float0:
    return lambda _: np.zeros(global_aval.shape, dtypes.float0)  # type: ignore
  if core.is_opaque_dtype(global_aval.dtype):
    return global_aval.dtype._rules.global_sharded_result_handler(
        global_aval, out_sharding, committed, is_out_sharding_from_xla)
  if xla_extension_version >= 131:
    return xc.array_result_handler(
        global_aval, out_sharding, committed=committed, _skip_checks=True
    )
  return lambda bufs: ArrayImpl(global_aval, out_sharding, bufs,
                                committed=committed, _skip_checks=True)
