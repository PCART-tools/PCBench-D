def ones(shape: Any, dtype: DTypeLike | None = None, *,
         device: xc.Device | Sharding | None = None) -> Array:
  """Create an array full of ones.

  JAX implementation of :func:`numpy.ones`.

  Args:
    shape: int or sequence of ints specifying the shape of the created array.
    dtype: optional dtype for the created array; defaults to floating point.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.ones_like`
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.zeros`
    - :func:`jax.numpy.full`

  Examples:
    >>> jnp.ones(4)
    Array([1., 1., 1., 1.], dtype=float32)
    >>> jnp.ones((2, 3), dtype=bool)
    Array([[ True,  True,  True],
           [ True,  True,  True]], dtype=bool)
  """
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  if (m := _check_forgot_shape_tuple("ones", shape, dtype)): raise TypeError(m)
  shape = canonicalize_shape(shape)
  dtypes.check_user_dtype_supported(dtype, "ones")
  return lax.full(shape, 1, _jnp_dtype(dtype), sharding=_normalize_to_sharding(device))
