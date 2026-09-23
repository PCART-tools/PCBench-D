@_wraps(np.polymul, lax_description=_LEADING_ZEROS_DOC)
def polymul(a1, a2, *, trim_leading_zeros=False):
  _check_arraylike("polymul", a1, a2)
  a1, a2 = _promote_dtypes_inexact(a1, a2)
  if trim_leading_zeros and (len(a1) > 1 or len(a2) > 1):
    a1, a2 = trim_zeros(a1, trim='f'), trim_zeros(a2, trim='f')
  if len(a1) == 0:
    a1 = asarray([0], dtype=a2.dtype)
  if len(a2) == 0:
    a2 = asarray([0], dtype=a1.dtype)
  return convolve(a1, a2, mode='full')
