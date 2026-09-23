@util.implements(np.copy, lax_description=_ARRAY_DOC)
def copy(a: ArrayLike, order: str | None = None) -> Array:
  util.check_arraylike("copy", a)
  return array(a, copy=True, order=order)
