def empty(shape: Any, dtype: DTypeLike | None = None, *,
          device: xc.Device | Sharding | None = None) -> Array:
  """Create an empty array.

  JAX implementation of :func:`numpy.empty`. Because XLA cannot create an
  un-initialized array, :func:`jax.numpy.empty` will always return an array
  full of zeros.

  Args:
    shape: int or sequence of ints specifying the shape of the created array.
    dtype: optional dtype for the created array; defaults to floating point.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.empty_like`
    - :func:`jax.numpy.zeros`
    - :func:`jax.numpy.ones`
    - :func:`jax.numpy.full`

  Examples:
    >>> jnp.empty(4)
    Array([0., 0., 0., 0.], dtype=float32)
    >>> jnp.empty((2, 3), dtype=bool)
    Array([[False, False, False],
           [False, False, False]], dtype=bool)
  """
  if (m := _check_forgot_shape_tuple("empty", shape, dtype)): raise TypeError(m)
  dtypes.check_user_dtype_supported(dtype, "empty")
  return zeros(shape, dtype, device=device)
