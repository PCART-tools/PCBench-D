@implements(np.poly, lax_description=_POLY_DOC)
@jit
def poly(seq_of_zeros: Array) -> Array:
  check_arraylike('poly', seq_of_zeros)
  seq_of_zeros, = promote_dtypes_inexact(seq_of_zeros)
  seq_of_zeros = atleast_1d(seq_of_zeros)

  sh = seq_of_zeros.shape
  if len(sh) == 2 and sh[0] == sh[1] and sh[0] != 0:
    # import at runtime to avoid circular import
    from jax._src.numpy import linalg
    seq_of_zeros = linalg.eigvals(seq_of_zeros)

  if seq_of_zeros.ndim != 1:
    raise ValueError("input must be 1d or non-empty square 2d array.")

  dt = seq_of_zeros.dtype
  if len(seq_of_zeros) == 0:
    return ones((), dtype=dt)

  a = ones((1,), dtype=dt)
  for k in range(len(seq_of_zeros)):
    a = convolve(a, array([1, -seq_of_zeros[k]], dtype=dt), mode='full')

  return a
