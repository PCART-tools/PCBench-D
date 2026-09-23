@partial(jit, static_argnames=('offset', 'axis1', 'axis2'))
def diagonal(a: ArrayLike, offset: int = 0, axis1: int = 0,
             axis2: int = 1) -> Array:
  """Returns the specified diagonal of an array.

  JAX implementation of :func:`numpy.diagonal`.

  The JAX version always returns a copy of the input, although if this is used
  within a JIT compilation, the compiler may avoid the copy.

  Args:
    a: Input array. Must be at least 2-dimensional.
    offset: optional, default=0. Diagonal offset from the main diagonal.
      Must be a static integer value. Can be positive or negative.
    axis1: optional, default=0. The first axis along which to take the diagonal.
    axis2: optional, default=1. The second axis along which to take the diagonal.

   Returns:
    A 1D array for 2D input, and in general a N-1 dimensional array
    for N-dimensional input.

  See also:
    - :func:`jax.numpy.diag`
    - :func:`jax.numpy.diagflat`

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> jnp.diagonal(x)
    Array([1, 5, 9], dtype=int32)
    >>> jnp.diagonal(x, offset=1)
    Array([2, 6], dtype=int32)
    >>> jnp.diagonal(x, offset=-1)
    Array([4, 8], dtype=int32)
  """
  util.check_arraylike("diagonal", a)
  a_shape = shape(a)
  if ndim(a) < 2:
    raise ValueError("diagonal requires an array of at least two dimensions.")
  offset = core.concrete_or_error(operator.index, offset, "'offset' argument of jnp.diagonal()")

  a = moveaxis(a, (axis1, axis2), (-2, -1))

  diag_size = max(0, min(a_shape[axis1] + min(offset, 0),
                         a_shape[axis2] - max(offset, 0)))
  i = arange(diag_size)
  j = arange(abs(offset), abs(offset) + diag_size)
  return a[..., i, j] if offset >= 0 else a[..., j, i]
