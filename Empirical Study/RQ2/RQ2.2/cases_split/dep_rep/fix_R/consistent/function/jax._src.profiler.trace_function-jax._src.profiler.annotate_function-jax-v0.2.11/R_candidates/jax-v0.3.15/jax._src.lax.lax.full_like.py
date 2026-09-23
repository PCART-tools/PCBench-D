def full_like(x: Array, fill_value: Array, dtype: Optional[DType] = None,
              shape: Optional[Shape] = None) -> Array:
  """Create a full array like np.full based on the example array `x`.

  Args:
    x: example array-like, used for shape and dtype information.
    fill_value: a scalar value to fill the entries of the output array.
    dtype: optional, a dtype parameter for the output ndarray.
    shape: optional, a shape parameter for the output ndarray.

  Returns:
    An ndarray with the same shape as `x` with its entries set equal to
    `fill_value`, similar to the output of np.full.
  """
  fill_shape = np.shape(x) if shape is None else canonicalize_shape(shape)
  weak_type = dtype is None and dtypes.is_weakly_typed(x)
  dtype = dtype or _dtype(x)
  return full(fill_shape, _convert_element_type(fill_value, dtype, weak_type))
