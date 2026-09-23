def _dummy_like(aval: core.AbstractValue) -> Any:
  if aval is core.abstract_token:
    return lax_internal.create_token()
  elif isinstance(aval, (core.ShapedArray, core.DShapedArray)):
    return lax_internal.broadcast(lax_internal.empty(aval.dtype), aval.shape)  # type: ignore
  else:
    raise ValueError(aval)
