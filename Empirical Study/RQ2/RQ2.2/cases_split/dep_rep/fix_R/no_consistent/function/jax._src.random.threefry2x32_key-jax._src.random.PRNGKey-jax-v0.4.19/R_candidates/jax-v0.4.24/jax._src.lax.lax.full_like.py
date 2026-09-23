def full_like(x: ArrayLike | DuckTypedArray,
              fill_value: ArrayLike, dtype: DTypeLike | None = None,
              shape: Shape | None = None, sharding: Sharding | None = None) -> Array:
  """Create a full array like np.full based on the example array `x`.

  Args:
    x: example array-like, used for shape and dtype information.
    fill_value: a scalar value to fill the entries of the output array.
    dtype: optional, a dtype parameter for the output ndarray.
    shape: optional, a shape parameter for the output ndarray.
    sharding: an optional sharding specification for the resulting array.
      If not specified, the output will have the same sharding as the input,
      so long as ``shape`` is also not specified.

  Returns:
    An ndarray with the same shape as `x` with its entries set equal to
    `fill_value`, similar to the output of np.full.
  """
  fill_shape = np.shape(x) if shape is None else canonicalize_shape(shape)  # type: ignore[arg-type]
  weak_type = dtype is None and dtypes.is_weakly_typed(x)
  dtype = dtype or _dtype(x)
  if dtypes.issubdtype(dtype, dtypes.extended):
    return dtype._rules.full(fill_shape, fill_value, dtype)  # type: ignore[union-attr]
  val = full(fill_shape, _convert_element_type(fill_value, dtype, weak_type),
             sharding=sharding)
  # TODO(yashkatariya): Use shard_like in tracing mode too i.e. remove the
  # ArrayImpl check.
  if shape is None and sharding is None and isinstance(x, array.ArrayImpl):
    if xla_extension_version < 227:
      sharding = x.sharding  # type: ignore[union-attr]
      if (not dispatch.is_single_device_sharding(sharding) and
          not isinstance(sharding, PmapSharding)):
        return array.make_array_from_callback(
            type_cast(array.Shape, fill_shape), sharding, lambda idx: val[idx])
    else:
      return shard_alike.shard_alike(x, val)[1]
  return val
