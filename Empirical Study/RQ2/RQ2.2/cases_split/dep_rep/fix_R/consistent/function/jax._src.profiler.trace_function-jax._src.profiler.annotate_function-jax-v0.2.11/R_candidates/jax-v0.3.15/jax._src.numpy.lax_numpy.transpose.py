@_wraps(np.transpose, lax_description=_ARRAY_VIEW_DOC)
def transpose(a, axes=None):
  _check_arraylike("transpose", a)
  axes = np.arange(ndim(a))[::-1] if axes is None else axes
  return lax.transpose(a, axes)
