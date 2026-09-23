def _cumulative_reduction(
    name: str, reduction: Callable[..., Array],
    a: ArrayLike, axis: int | None, dtype: DTypeLike | None, out: None,
    fill_nan: bool = False, fill_value: ArrayLike = 0,
    promote_integers: bool = False) -> Array:
  """Helper function for implementing cumulative reductions."""
  check_arraylike(name, a)
  if out is not None:
    raise NotImplementedError(f"The 'out' argument to jnp.{name} is not supported")
  dtypes.check_user_dtype_supported(dtype, name)

  if axis is None or _isscalar(a):
    a = lax.reshape(a, (np.size(a),))
  if axis is None:
    axis = 0

  a_shape = list(np.shape(a))
  num_dims = len(a_shape)
  axis = _canonicalize_axis(axis, num_dims)

  if fill_nan:
    a = _where(lax_internal._isnan(a), _lax_const(a, fill_value), a)

  result_type: DTypeLike = dtypes.dtype(dtype or a)
  if dtype is None and promote_integers or dtypes.issubdtype(result_type, np.bool_):
    result_type = _promote_integer_dtype(result_type)
  result_type = dtypes.canonicalize_dtype(result_type)

  a = lax.convert_element_type(a, result_type)
  result = reduction(a, axis)

  # We downcast to boolean because we accumulate in integer types
  if dtypes.issubdtype(dtype, np.bool_):
    result = lax.convert_element_type(result, np.bool_)
  return result
