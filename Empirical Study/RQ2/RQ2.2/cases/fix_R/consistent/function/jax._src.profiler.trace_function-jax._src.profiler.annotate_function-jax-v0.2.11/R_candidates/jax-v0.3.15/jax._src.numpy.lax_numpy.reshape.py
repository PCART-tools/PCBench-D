@_wraps(np.reshape, lax_description=_ARRAY_VIEW_DOC)
def reshape(a, newshape, order="C"):
  _stackable(a) or _check_arraylike("reshape", a)
  try:
    return a.reshape(newshape, order=order)  # forward to method for ndarrays
  except AttributeError:
    return _reshape(a, newshape, order=order)
