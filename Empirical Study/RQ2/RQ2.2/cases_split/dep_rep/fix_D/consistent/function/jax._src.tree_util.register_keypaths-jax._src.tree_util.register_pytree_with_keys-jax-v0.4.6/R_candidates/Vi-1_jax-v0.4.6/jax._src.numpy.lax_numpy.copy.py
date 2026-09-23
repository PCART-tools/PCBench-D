@util._wraps(np.copy, lax_description=_ARRAY_DOC)
def copy(a: ArrayLike, order: Optional[str] = None) -> Array:
  util._check_arraylike("copy", a)
  return array(a, copy=True, order=order)
