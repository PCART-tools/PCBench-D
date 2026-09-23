def full_like(a: ArrayLike | DuckTypedArray,
              fill_value: ArrayLike, dtype: DTypeLike | None = None,
              shape: Any = None, *,
              device: xc.Device | Sharding | None = None) -> Array:
  """Create an array full of a specified value with the same shape and dtype as an array.

  JAX implementation of :func:`numpy.full_like`.

  Args:
    a: Array-like object with ``shape`` and ``dtype`` attributes.
    fill_value: scalar or array with which to fill the created array.
    shape: optionally override the shape of the created array.
    dtype: optionally override the dtype of the created array.
    device: (optional) :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Array of the specified shape and dtype, on the specified device if specified.

  See also:
    - :func:`jax.numpy.full`
    - :func:`jax.numpy.empty_like`
    - :func:`jax.numpy.zeros_like`
    - :func:`jax.numpy.ones_like`

  Examples:
    >>> x = jnp.arange(4.0)
    >>> jnp.full_like(x, 2)
    Array([2., 2., 2., 2.], dtype=float32)
    >>> jnp.full_like(x, 0, shape=(2, 3))
    Array([[0., 0., 0.],
           [0., 0., 0.]], dtype=float32)

    `fill_value` may also be an array that is broadcast to the specified shape:

    >>> x = jnp.arange(6).reshape(2, 3)
    >>> jnp.full_like(x, fill_value=jnp.array([[1], [2]]))
    Array([[1, 1, 1],
           [2, 2, 2]], dtype=int32)
  """
  if hasattr(a, 'dtype') and hasattr(a, 'shape'):  # support duck typing
    util.check_arraylike("full_like", 0, fill_value)
  else:
    util.check_arraylike("full_like", a, fill_value)
  dtypes.check_user_dtype_supported(dtype, "full_like")
  if shape is not None:
    shape = canonicalize_shape(shape)
  if ndim(fill_value) == 0:
    return lax.full_like(a, fill_value, dtype, shape, sharding=_normalize_to_sharding(device))
  else:
    shape = np.shape(a) if shape is None else shape  # type: ignore[arg-type]
    dtype = result_type(a) if dtype is None else dtype
    return jax.device_put(
        broadcast_to(asarray(fill_value, dtype=dtype), shape), device)
