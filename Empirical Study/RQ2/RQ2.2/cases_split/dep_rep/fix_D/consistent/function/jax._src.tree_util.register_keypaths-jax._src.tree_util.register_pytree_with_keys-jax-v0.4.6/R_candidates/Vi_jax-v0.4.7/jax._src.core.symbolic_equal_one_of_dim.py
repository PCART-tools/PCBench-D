def symbolic_equal_one_of_dim(d1: DimSize, dlist: Sequence[DimSize]) -> bool:
  if any(d1 is d for d in dlist): return True  # identical always implies equal
  handler, ds = _dim_handler_and_canonical(d1, *dlist)
  return any([handler.symbolic_equal(ds[0], d) for d in ds[1:]])
