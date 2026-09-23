def identity(n: DimSize, dtype: DTypeLike | None = None) -> Array:
  """Create a square identity matrix

  JAX implementation of :func:`numpy.identity`.

  Args:
    n: integer specifying the size of each array dimension.
    dtype: optional dtype; defaults to floating point.

  Returns:
    Identity array of shape ``(n, n)``.

  See also:
    :func:`jax.numpy.eye`: non-square and/or offset identity matrices.

  Examples:
    A simple 3x3 identity matrix:

    >>> jnp.identity(3)
    Array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]], dtype=float32)

    A 2x2 integer identity matrix:

    >>> jnp.identity(2, dtype=int)
    Array([[1, 0],
           [0, 1]], dtype=int32)
  """
  dtypes.check_user_dtype_supported(dtype, "identity")
  return eye(n, dtype=dtype)
