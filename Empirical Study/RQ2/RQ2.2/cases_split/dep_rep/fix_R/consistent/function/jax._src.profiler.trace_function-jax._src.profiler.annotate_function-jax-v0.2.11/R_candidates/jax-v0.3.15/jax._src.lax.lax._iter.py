def _iter(tracer):
  if tracer.ndim == 0:
    raise TypeError("iteration over a 0-d array")  # same as numpy error
  else:
    n = int(tracer.shape[0])
    # return (index_in_dim(tracer, i, keepdims=False) for i in range(n))
    return iter([slicing.index_in_dim(tracer, i, keepdims=False)
                 for i in range(n)])
