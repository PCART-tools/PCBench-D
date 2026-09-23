@util._wraps(np.diag_indices_from)
def diag_indices_from(arr: ArrayLike) -> tuple[Array, ...]:
  util.check_arraylike("diag_indices_from", arr)
  nd = ndim(arr)
  if not ndim(arr) >= 2:
    raise ValueError("input array must be at least 2-d")

  s = shape(arr)
  if len(set(shape(arr))) != 1:
    raise ValueError("All dimensions of input must be of equal length")

  return diag_indices(s[0], ndim=nd)
