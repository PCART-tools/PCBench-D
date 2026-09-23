def _array_local_result_handler(aval, sharding, indices):
  if aval.dtype == dtypes.float0:
    return lambda _: np.zeros(aval.shape, dtypes.float0)  # type: ignore
  if core.is_opaque_dtype(aval.dtype):
    return aval.dtype._rules.local_sharded_result_handler(
        aval, sharding, indices)
  if xla_extension_version >= 131:
    return xc.array_result_handler(
        aval, sharding, committed=True, _skip_checks=True
    )
  return lambda bufs: ArrayImpl(aval, sharding, bufs, committed=True,
                                _skip_checks=True)
