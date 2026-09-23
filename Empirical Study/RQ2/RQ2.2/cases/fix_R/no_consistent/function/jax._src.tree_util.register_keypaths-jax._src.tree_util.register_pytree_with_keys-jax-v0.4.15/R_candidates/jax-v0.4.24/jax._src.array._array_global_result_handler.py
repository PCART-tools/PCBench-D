def _array_global_result_handler(global_aval, out_sharding, committed,
                                 is_out_sharding_from_xla):
  if global_aval.dtype == dtypes.float0:
    return lambda _: np.zeros(global_aval.shape, dtypes.float0)  # type: ignore
  if dtypes.issubdtype(global_aval.dtype, dtypes.extended):
    return global_aval.dtype._rules.global_sharded_result_handler(
        global_aval, out_sharding, committed, is_out_sharding_from_xla)
  return xc.array_result_handler(
      global_aval, out_sharding, committed=committed, _skip_checks=True
  )
