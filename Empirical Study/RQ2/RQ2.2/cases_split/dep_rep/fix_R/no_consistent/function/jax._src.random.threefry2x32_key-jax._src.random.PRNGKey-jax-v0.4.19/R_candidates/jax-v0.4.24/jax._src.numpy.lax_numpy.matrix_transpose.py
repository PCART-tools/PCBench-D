@util.implements(getattr(np, 'matrix_transpose', None))
def matrix_transpose(x: ArrayLike, /) -> Array:
  """Transposes the last two dimensions of x.

  Parameters
  ----------
  x : array_like
      Input array. Must have ``x.ndim >= 2``.

  Returns
  -------
  xT : Array
      Transposed array.
  """
  util.check_arraylike("matrix_transpose", x)
  ndim = np.ndim(x)
  if ndim < 2:
    raise ValueError(f"x must be at least two-dimensional for matrix_transpose; got {ndim=}")
  axes = (*range(ndim - 2), ndim - 1, ndim - 2)
  return lax.transpose(x, axes)
