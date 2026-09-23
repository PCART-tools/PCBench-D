@util.implements(np.flipud, lax_description=_ARRAY_VIEW_DOC)
def flipud(m: ArrayLike) -> Array:
  util.check_arraylike("flipud", m)
  return _flip(asarray(m), 0)
