def to_default_dtype(arr):
  """Convert a value to an array with JAX's default dtype.

  This is generally used for type conversions of values returned by numpy functions,
  to make their dtypes take into account the state of the ``jax_enable_x64`` and
  ``jax_default_dtype_bits`` flags.
  """
  arr = np.asarray(arr)
  dtype = _dtypes._default_types.get(arr.dtype.kind)
  return arr.astype(_dtypes.canonicalize_dtype(dtype)) if dtype else arr
