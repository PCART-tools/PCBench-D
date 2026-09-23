def _infer_src_sharding(src, x) -> Sharding | None:
  if src is not None:
    return src
  if isinstance(x, array.ArrayImpl):
    return x.sharding
  elif isinstance(x, core.Tracer):
    aval = core.get_aval(x)
    if isinstance(aval, ConcreteArray) and isinstance(aval.val, array.ArrayImpl):
      return aval.val.sharding
  return None
