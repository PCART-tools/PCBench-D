@util.implements(np.fliplr, lax_description=_ARRAY_VIEW_DOC)
def fliplr(m: ArrayLike) -> Array:
  util.check_arraylike("fliplr", m)
  return _flip(asarray(m), 1)
