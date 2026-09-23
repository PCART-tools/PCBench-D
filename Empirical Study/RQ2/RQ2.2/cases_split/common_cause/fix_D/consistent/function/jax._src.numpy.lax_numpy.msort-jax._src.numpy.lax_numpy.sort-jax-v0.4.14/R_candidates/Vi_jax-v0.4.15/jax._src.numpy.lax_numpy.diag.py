@util._wraps(np.diag, lax_description=_ARRAY_VIEW_DOC)
def diag(v: ArrayLike, k: int = 0) -> Array:
  return _diag(v, operator.index(k))
