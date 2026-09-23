def _iter(tracer):
  if tracer.ndim == 0:
    raise TypeError("iteration over a 0-d array")  # same as numpy error
  else:
    n = int(tracer.shape[0])
    if any(isinstance(d, core.Tracer) for d in tracer.shape):
      return (slicing.dynamic_index_in_dim(tracer, i, keepdims=False)
              for i in range(n))
    else:
      return (slicing.index_in_dim(tracer, i, keepdims=False) for i in range(n))
