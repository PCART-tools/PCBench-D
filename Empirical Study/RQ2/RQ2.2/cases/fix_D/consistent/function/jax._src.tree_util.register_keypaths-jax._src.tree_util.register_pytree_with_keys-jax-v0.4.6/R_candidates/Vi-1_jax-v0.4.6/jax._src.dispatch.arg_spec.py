def arg_spec(x: Any) -> ArgSpec:
  from jax._src import pjit

  aval = xla.abstractify(x)
  try:
    if config.jax_array:
      if isinstance(x.sharding, PmapSharding):
        return aval, None
      return aval, (pjit.to_gspmd_sharding(x.sharding, x.ndim)  # type: ignore
                    if x._committed else None)
    else:
      return aval, x._device
  except:
    return aval, None
