@_wraps(np.ediff1d, lax_description=_EDIFF1D_DOC)
@jit
def ediff1d(ary, to_end=None, to_begin=None):
  _check_arraylike("ediff1d", ary)
  ary = ravel(ary)
  result = lax.sub(ary[1:], ary[:-1])
  if to_begin is not None:
    _check_arraylike("ediff1d", to_begin)
    result = concatenate((ravel(asarray(to_begin, dtype=ary.dtype)), result))
  if to_end is not None:
    _check_arraylike("ediff1d", to_end)
    result = concatenate((result, ravel(asarray(to_end, dtype=ary.dtype))))
  return result
