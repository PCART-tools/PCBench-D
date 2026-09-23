@util._wraps(np.flipud, lax_description=_ARRAY_VIEW_DOC)
def flipud(m: ArrayLike) -> Array:
  util._check_arraylike("flipud", m)
  return _flip(asarray(m), 0)
