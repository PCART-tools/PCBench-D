def _infer_src_sharding(src, x):
  if src is not None:
    return src
  return x.sharding if isinstance(x, array.ArrayImpl) else None
