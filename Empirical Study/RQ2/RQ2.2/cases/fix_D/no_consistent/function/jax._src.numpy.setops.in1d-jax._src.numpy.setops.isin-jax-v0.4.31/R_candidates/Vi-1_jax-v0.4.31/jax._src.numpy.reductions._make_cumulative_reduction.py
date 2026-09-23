def _make_cumulative_reduction(np_reduction: Any, reduction: Callable[..., Array],
                               fill_nan: bool = False, fill_value: ArrayLike = 0,
                               promote_integers: bool = False) -> CumulativeReduction:
  @implements(np_reduction, skip_params=['out'],
          lax_description=CUML_REDUCTION_LAX_DESCRIPTION)
  def cumulative_reduction(a: ArrayLike, axis: Axis = None,
                           dtype: DTypeLike | None = None, out: None = None) -> Array:
    return _cumulative_reduction(a, _ensure_optional_axes(axis), dtype, out)

  @partial(api.jit, static_argnames=('axis', 'dtype'))
  def _cumulative_reduction(a: ArrayLike, axis: Axis = None,
                            dtype: DTypeLike | None = None, out: None = None) -> Array:
    check_arraylike(np_reduction.__name__, a)
    if out is not None:
      raise NotImplementedError(f"The 'out' argument to jnp.{np_reduction.__name__} "
                                f"is not supported.")
    dtypes.check_user_dtype_supported(dtype, np_reduction.__name__)

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

  return cumulative_reduction
