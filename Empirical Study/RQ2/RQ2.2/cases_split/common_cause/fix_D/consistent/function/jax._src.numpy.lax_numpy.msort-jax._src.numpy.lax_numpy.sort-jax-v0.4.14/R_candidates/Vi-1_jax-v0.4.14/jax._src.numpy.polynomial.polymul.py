@_wraps(np.polymul, lax_description=_LEADING_ZEROS_DOC)
def polymul(a1: ArrayLike, a2: ArrayLike, *, trim_leading_zeros: bool = False) -> Array:
  check_arraylike("polymul", a1, a2)
  a1_arr, a2_arr = promote_dtypes_inexact(a1, a2)
  if trim_leading_zeros and (len(a1_arr) > 1 or len(a2_arr) > 1):
    a1_arr, a2_arr = trim_zeros(a1_arr, trim='f'), trim_zeros(a2_arr, trim='f')
  if len(a1_arr) == 0:
    a1_arr = asarray([0], dtype=a2_arr.dtype)
  if len(a2_arr) == 0:
    a2_arr = asarray([0], dtype=a1_arr.dtype)
  return convolve(a1_arr, a2_arr, mode='full')
