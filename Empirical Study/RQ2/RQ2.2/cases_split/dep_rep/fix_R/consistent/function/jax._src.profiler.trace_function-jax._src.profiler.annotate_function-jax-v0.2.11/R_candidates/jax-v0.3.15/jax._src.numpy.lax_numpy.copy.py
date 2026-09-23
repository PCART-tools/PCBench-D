@_wraps(np.copy, lax_description=_ARRAY_DOC)
def copy(a, order=None):
  return array(a, copy=True, order=order)
