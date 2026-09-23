@util._wraps(np.reshape, lax_description=_ARRAY_VIEW_DOC)
def reshape(a: ArrayLike, newshape: DimSize | Shape, order: str = "C") -> Array:
  util.check_arraylike("reshape", a)
  try:
    # forward to method for ndarrays
    return a.reshape(newshape, order=order)  # type: ignore[call-overload,union-attr]
  except AttributeError:
    return asarray(a).reshape(newshape, order=order)
