@util.implements(np.reshape, lax_description=_ARRAY_VIEW_DOC)
def reshape(a: ArrayLike, newshape: DimSize | Shape, order: str = "C") -> Array:
  __tracebackhide__ = True
  util.check_arraylike("reshape", a)
  try:
    # forward to method for ndarrays
    return a.reshape(newshape, order=order)  # type: ignore[call-overload,union-attr]
  except AttributeError:
    pass
  return asarray(a).reshape(newshape, order=order)
