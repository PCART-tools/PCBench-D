def bernoulli(key: KeyArray,
              p: RealArray = np.float32(0.5),
              shape: Optional[Union[Shape, NamedShape]] = None) -> Array:
  """Sample Bernoulli random values with given shape and mean.

  Args:
    key: a PRNG key used as the random key.
    p: optional, a float or array of floats for the mean of the random
      variables. Must be broadcast-compatible with ``shape``. Default 0.5.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Must be broadcast-compatible with ``p.shape``. The default (None)
      produces a result shape equal to ``p.shape``.

  Returns:
    A random array with boolean dtype and shape given by ``shape`` if ``shape``
    is not None, or else ``p.shape``.
  """
  key, _ = _check_prng_key(key)
  dtype = dtypes.canonicalize_dtype(lax.dtype(p))
  if shape is not None:
    shape = core.as_named_shape(shape)
  if not jnp.issubdtype(dtype, np.floating):
    msg = "bernoulli probability `p` must have a floating dtype, got {}."
    raise TypeError(msg.format(dtype))
  p = lax.convert_element_type(p, dtype)
  return _bernoulli(key, p, shape)  # type: ignore
