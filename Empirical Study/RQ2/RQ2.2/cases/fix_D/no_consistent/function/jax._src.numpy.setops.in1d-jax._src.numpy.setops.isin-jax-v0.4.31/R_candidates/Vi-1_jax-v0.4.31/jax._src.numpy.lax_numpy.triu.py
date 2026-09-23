@partial(jit, static_argnames=('k',))
def triu(m: ArrayLike, k: int = 0) -> Array:
  r"""Return upper triangle of an array.

  JAX implementation of :func:`numpy.triu`

  Args:
    m: input array. Must have ``m.ndim >= 2``.
    k: optional, int, default=0. Specifies the sub-diagonal below which the
      elements of the array are set to zero. ``k=0`` refers to main diagonal,
      ``k<0`` refers to sub-diagonal below the main diagonal and ``k>0`` refers
      to sub-diagonal above the main diagonal.

  Returns:
    An array with same shape as input containing the lower triangle of the given
    array with elements above the sub-diagonal specified by ``k`` are set to zero.

  See also:
    - :func:`jax.numpy.tril`: Returns a lower triangle of an array.
    - :func:`jax.numpy.tri`: Returns an array with ones on and below the diagonal
      and zeros elsewhere.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9],
    ...                [10, 11, 12]])
    >>> jnp.triu(x)
    Array([[1, 2, 3],
           [0, 5, 6],
           [0, 0, 9],
           [0, 0, 0]], dtype=int32)
    >>> jnp.triu(x, k=1)
    Array([[0, 2, 3],
           [0, 0, 6],
           [0, 0, 0],
           [0, 0, 0]], dtype=int32)
    >>> jnp.triu(x, k=-1)
    Array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 0,  8,  9],
           [ 0,  0, 12]], dtype=int32)

    When ``m.ndim > 2``, ``jnp.triu`` operates batch-wise on the trailing axes.

    >>> x1 = jnp.array([[[1, 2],
    ...                  [3, 4]],
    ...                 [[5, 6],
    ...                  [7, 8]]])
    >>> jnp.triu(x1)
    Array([[[1, 2],
            [0, 4]],
    <BLANKLINE>
           [[5, 6],
            [0, 8]]], dtype=int32)
  """
  util.check_arraylike("triu", m)
  m_shape = shape(m)
  if len(m_shape) < 2:
    raise ValueError("Argument to jax.numpy.triu must be at least 2D")
  N, M = m_shape[-2:]
  mask = tri(N, M, k=k - 1, dtype=bool)
  return lax.select(lax.broadcast(mask, m_shape[:-2]), zeros_like(m), m)
