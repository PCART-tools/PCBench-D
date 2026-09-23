def ones_like(a: ArrayLike | DuckTypedArray,
              dtype: DTypeLike | None = None,
              shape: Any = None, *,
              device: xc.Device | Sharding | None = None) -> Array:
  """Create an array of ones with the same shape and dtype as an array.

  JAX implementation of :func:`numpy.ones_like`.

  Args:
    a: Array-like object with ``shape`` and ``dtype`` attributes.
    shape: optionally override the shape of the created array.
    dtype: optionally override the dtype of the created array.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.empty`
    - :func:`jax.numpy.zeros_like`
    - :func:`jax.numpy.ones_like`
    - :func:`jax.numpy.full_like`

  Examples:
    >>> x = jnp.arange(4)
    >>> jnp.ones_like(x)
    Array([1, 1, 1, 1], dtype=int32)
    >>> jnp.ones_like(x, dtype=bool)
    Array([ True,  True,  True,  True], dtype=bool)
    >>> jnp.ones_like(x, shape=(2, 3))
    Array([[1, 1, 1],
           [1, 1, 1]], dtype=int32)
  """
  if not (hasattr(a, 'dtype') and hasattr(a, 'shape')):  # support duck typing
    util.check_arraylike("ones_like", a)
  dtypes.check_user_dtype_supported(dtype, "ones_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  return lax.full_like(a, 1, dtype, shape, sharding=_normalize_to_sharding(device))
