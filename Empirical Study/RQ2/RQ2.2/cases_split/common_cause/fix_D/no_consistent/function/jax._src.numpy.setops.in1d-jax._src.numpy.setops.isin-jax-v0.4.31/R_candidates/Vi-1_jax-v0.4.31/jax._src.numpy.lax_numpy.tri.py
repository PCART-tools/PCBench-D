def tri(N: int, M: int | None = None, k: int = 0, dtype: DTypeLike | None = None) -> Array:
  r"""Return an array with ones on and below the diagonal and zeros elsewhere.

  JAX implementation of :func:`numpy.tri`

  Args:
    N: int. Dimension of the rows of the returned array.
    M: optional, int. Dimension of the columns of the returned array. If not
      specified, then ``M = N``.
    k: optional, int, default=0. Specifies the sub-diagonal on and below which
      the array is filled with ones. ``k=0`` refers to main diagonal, ``k<0``
      refers to sub-diagonal below the main diagonal and ``k>0`` refers to
      sub-diagonal above the main diagonal.
    dtype: optional, data type of the returned array. The default type is float.

  Returns:
    An array of shape ``(N, M)`` containing the lower triangle with elements
    below the sub-diagonal specified by ``k`` are set to one and zero elsewhere.

  See also:
    - :func:`jax.numpy.tril`: Returns a lower triangle of an array.
    - :func:`jax.numpy.triu`: Returns an upper triangle of an array.

  Examples:
    >>> jnp.tri(3)
    Array([[1., 0., 0.],
           [1., 1., 0.],
           [1., 1., 1.]], dtype=float32)

    When ``M`` is not equal to ``N``:

    >>> jnp.tri(3, 4)
    Array([[1., 0., 0., 0.],
           [1., 1., 0., 0.],
           [1., 1., 1., 0.]], dtype=float32)

    when ``k>0``:

    >>> jnp.tri(3, k=1)
    Array([[1., 1., 0.],
           [1., 1., 1.],
           [1., 1., 1.]], dtype=float32)

    When ``k<0``:

    >>> jnp.tri(3, 4, k=-1)
    Array([[0., 0., 0., 0.],
           [1., 0., 0., 0.],
           [1., 1., 0., 0.]], dtype=float32)
  """
  dtypes.check_user_dtype_supported(dtype, "tri")
  M = M if M is not None else N
  dtype = dtype or float32
  return lax_internal._tri(dtype, (N, M), k)
