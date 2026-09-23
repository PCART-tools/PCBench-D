def full(shape: Shape, fill_value: ArrayLike, dtype: DTypeLike | None = None, *,
         sharding: Sharding | None = None) -> Array:
  """Returns an array of `shape` filled with `fill_value`.

  Args:
    shape: sequence of integers, describing the shape of the output array.
    fill_value: the value to fill the new array with.
    dtype: the type of the output array, or `None`. If not `None`, `fill_value`
      will be cast to `dtype`.
    sharding: an optional sharding specification for the resulting array.
  """
  shape = canonicalize_shape(shape)
  if np.shape(fill_value):
    msg = "full must be called with scalar fill_value, got fill_value.shape {}."
    raise TypeError(msg.format(np.shape(fill_value)))
  if dtypes.issubdtype(dtype, dtypes.extended):
    return dtype._rules.full(shape, fill_value, dtype)  # type: ignore[union-attr]
  weak_type = dtype is None and dtypes.is_weakly_typed(fill_value)
  dtype = dtypes.canonicalize_dtype(dtype or _dtype(fill_value))
  fill_value = _convert_element_type(fill_value, dtype, weak_type)
  out = broadcast(fill_value, shape)
  if sharding is not None:
    return array.make_array_from_callback(shape, sharding, lambda idx: out[idx])
  return out
