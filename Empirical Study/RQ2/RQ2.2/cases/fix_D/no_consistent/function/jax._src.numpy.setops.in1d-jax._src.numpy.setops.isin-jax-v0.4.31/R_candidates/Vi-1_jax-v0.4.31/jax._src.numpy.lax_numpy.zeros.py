def zeros(shape: Any, dtype: DTypeLike | None = None, *,
          device: xc.Device | Sharding | None = None) -> Array:
  """Create an array full of zeros.

  JAX implementation of :func:`numpy.zeros`.

  Args:
    shape: int or sequence of ints specifying the shape of the created array.
    dtype: optional dtype for the created array; defaults to floating point.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.zeros_like`
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.ones`
    - :func:`jax.numpy.full`

  Examples:
    >>> jnp.zeros(4)
    Array([0., 0., 0., 0.], dtype=float32)
    >>> jnp.zeros((2, 3), dtype=bool)
    Array([[False, False, False],
           [False, False, False]], dtype=bool)
  """
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  if (m := _check_forgot_shape_tuple("zeros", shape, dtype)): raise TypeError(m)
  dtypes.check_user_dtype_supported(dtype, "zeros")
  shape = canonicalize_shape(shape)
  return lax.full(shape, 0, _jnp_dtype(dtype), sharding=_normalize_to_sharding(device))
