def arg_spec(x: Any) -> ArgSpec:
  from jax._src import pjit

  aval = xla.abstractify(x)
  try:
    if isinstance(x.sharding, PmapSharding):
      return aval, None
    return aval, (pjit.to_gspmd_sharding(x.sharding, x.ndim)  # type: ignore
                  if x._committed else None)
  except:
    return aval, None
