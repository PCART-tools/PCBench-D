def full(shape: Any, fill_value: ArrayLike,
         dtype: DTypeLike | None = None, *,
         device: xc.Device | Sharding | None = None) -> Array:
  """Create an array full of a specified value.

  JAX implementation of :func:`numpy.full`.

  Args:
    shape: int or sequence of ints specifying the shape of the created array.
    fill_value: scalar or array with which to fill the created array.
    dtype: optional dtype for the created array; defaults to the dtype of the
      fill value.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.full_like`
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.zeros`
    - :func:`jax.numpy.ones`

  Examples:
    >>> jnp.full(4, 2, dtype=float)
    Array([2., 2., 2., 2.], dtype=float32)
    >>> jnp.full((2, 3), 0, dtype=bool)
    Array([[False, False, False],
           [False, False, False]], dtype=bool)

    `fill_value` may also be an array that is broadcast to the specified shape:

    >>> jnp.full((2, 3), fill_value=jnp.arange(3))
    Array([[0, 1, 2],
           [0, 1, 2]], dtype=int32)
  """
  dtypes.check_user_dtype_supported(dtype, "full")
  util.check_arraylike("full", fill_value)

  if ndim(fill_value) == 0:
    shape = canonicalize_shape(shape)
    return lax.full(shape, fill_value, dtype, sharding=_normalize_to_sharding(device))
  else:
    return jax.device_put(
        broadcast_to(asarray(fill_value, dtype=dtype), shape), device)
