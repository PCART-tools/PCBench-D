def diag_indices(n: int, ndim: int = 2) -> tuple[Array, ...]:
  """Return indices for accessing the main diagonal of a multidimensional array.

  JAX implementation of :func:`numpy.diag_indices`.

  Args:
    n: int. The size of each dimension of the square array.
    ndim: optional, int, default=2. The number of dimensions of the array.

  Returns:
    A tuple of arrays, each of length `n`, containing the indices to access
    the main diagonal.

  See also:
    - :func:`jax.numpy.diag_indices_from`
    - :func:`jax.numpy.diagonal`

  Examples:
    >>> jnp.diag_indices(3)
    (Array([0, 1, 2], dtype=int32), Array([0, 1, 2], dtype=int32))
    >>> jnp.diag_indices(4, ndim=3)
    (Array([0, 1, 2, 3], dtype=int32),
    Array([0, 1, 2, 3], dtype=int32),
    Array([0, 1, 2, 3], dtype=int32))
  """
  n = core.concrete_or_error(operator.index, n, "'n' argument of jnp.diag_indices()")
  ndim = core.concrete_or_error(operator.index, ndim, "'ndim' argument of jnp.diag_indices()")
  if n < 0:
    raise ValueError("n argument to diag_indices must be nonnegative, got {}"
                     .format(n))
  if ndim < 0:
    raise ValueError("ndim argument to diag_indices must be nonnegative, got {}"
                     .format(ndim))
  return (lax.iota(int_, n),) * ndim
