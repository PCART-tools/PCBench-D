def full_like(x: ArrayLike, fill_value: ArrayLike, dtype: Optional[DTypeLike] = None,
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
  val = full(fill_shape, _convert_element_type(fill_value, dtype, weak_type))
  # If the sharding is SingleDeviceSharding then don't take the `if` branch
  # because `val` is already an array with SingleDeviceSharding making this an
  # optimization.
  # TODO(yashkatariya,mattjj): `x` and `val` should have the same sharding,
  # probably in the form of a primitive like `val = match_sharding_p.bind(x, val)`
  # (so it works in staged-out code as well as 'eager' code). Related to
  # equi-sharding.
  if shape is None and isinstance(x, array.ArrayImpl):
    sharding = x.sharding  # type: ignore[union-attr]
    if (not dispatch.is_single_device_sharding(sharding) and
        not isinstance(sharding, PmapSharding)):
      return array.make_array_from_callback(
          type_cast(array.Shape, fill_shape), sharding, lambda idx: val[idx])
  return val
