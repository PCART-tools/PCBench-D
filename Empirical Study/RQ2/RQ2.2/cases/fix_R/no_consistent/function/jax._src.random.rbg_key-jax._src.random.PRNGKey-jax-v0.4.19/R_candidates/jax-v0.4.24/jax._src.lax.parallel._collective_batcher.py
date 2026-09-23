def _collective_batcher(prim, args, dims, **params):
  return prim.bind(*args, **params), dims if prim.multiple_results else dims[0]
