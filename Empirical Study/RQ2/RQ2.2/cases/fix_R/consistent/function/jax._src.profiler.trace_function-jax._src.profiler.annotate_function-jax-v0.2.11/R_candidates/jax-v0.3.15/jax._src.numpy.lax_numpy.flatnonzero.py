@_wraps(np.flatnonzero, lax_description=_NONZERO_DOC, extra_params=_NONZERO_EXTRA_PARAMS)
def flatnonzero(a, *, size=None, fill_value=None):
  return nonzero(ravel(a), size=size, fill_value=fill_value)[0]
