def _array_local_result_handler(aval, sharding, indices):
  if aval.dtype == dtypes.float0:
    return lambda _: np.zeros(aval.shape, dtypes.float0)  # type: ignore
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    return aval.dtype._rules.local_sharded_result_handler(
        aval, sharding, indices)
  return xc.array_result_handler(
      aval, sharding, committed=True, _skip_checks=True
  )
