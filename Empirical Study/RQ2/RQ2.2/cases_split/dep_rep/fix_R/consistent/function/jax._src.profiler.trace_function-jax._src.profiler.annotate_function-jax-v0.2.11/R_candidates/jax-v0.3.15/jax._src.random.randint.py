def randint(key: KeyArray,
            shape: Sequence[int],
            minval: IntegerArray,
            maxval: IntegerArray,
            dtype: DTypeLikeInt = dtypes.int_):
  """Sample uniform random values in [minval, maxval) with given shape/dtype.

  Args:
    key: a PRNG key used as the random key.
    shape: a tuple of nonnegative integers representing the shape.
    minval: int or array of ints broadcast-compatible with ``shape``, a minimum
      (inclusive) value for the range.
    maxval: int or array of ints broadcast-compatible with ``shape``, a maximum
      (exclusive) value for the range.
    dtype: optional, an int dtype for the returned values (default int64 if
      jax_enable_x64 is true, otherwise int32).

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key(key)
  dtype = dtypes.canonicalize_dtype(dtype)
  shape = core.canonicalize_shape(shape)
  return _randint(key, shape, minval, maxval, dtype)
