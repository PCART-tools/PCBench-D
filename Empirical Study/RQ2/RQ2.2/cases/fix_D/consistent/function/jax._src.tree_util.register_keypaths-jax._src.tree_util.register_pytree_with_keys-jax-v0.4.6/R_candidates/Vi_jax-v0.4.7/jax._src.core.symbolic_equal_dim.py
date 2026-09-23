def symbolic_equal_dim(d1: DimSize, d2: DimSize) -> bool:
  if d1 is d2 or get_referent(d1) is get_referent(d2): return True
  handler, ds = _dim_handler_and_canonical(d1, d2)
  return handler.symbolic_equal(*ds)
