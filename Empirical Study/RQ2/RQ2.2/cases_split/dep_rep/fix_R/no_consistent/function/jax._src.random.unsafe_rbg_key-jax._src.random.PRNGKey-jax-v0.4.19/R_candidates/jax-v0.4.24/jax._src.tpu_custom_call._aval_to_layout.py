def _aval_to_layout(aval):
  arange = np.arange(aval.ndim, dtype=np.dtype(np.int64))[::-1].copy()
  return ir.DenseIntElementsAttr.get(arange, type=ir.IndexType.get())
