def _arg_spec(x: Any) -> _ArgSpec:
  from jax._src import pjit

  aval = xla.abstractify(x)
  try:
    if isinstance(x.sharding, PmapSharding):
      return _ArgSpec(aval, None)
    return _ArgSpec(aval, (pjit.to_gspmd_sharding(x.sharding, x.ndim)  # type: ignore
                          if x._committed else None))
  except:
    return _ArgSpec(aval, None)
