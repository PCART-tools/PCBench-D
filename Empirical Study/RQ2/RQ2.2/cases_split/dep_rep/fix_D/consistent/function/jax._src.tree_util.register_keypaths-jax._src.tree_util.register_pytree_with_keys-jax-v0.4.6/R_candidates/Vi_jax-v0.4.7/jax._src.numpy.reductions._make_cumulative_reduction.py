def _make_cumulative_reduction(np_reduction: Any, reduction: Callable[..., Array],
                               fill_nan: bool = False, fill_value: ArrayLike = 0) -> Callable[..., Array]:
  @_wraps(np_reduction, skip_params=['out'])
  def cumulative_reduction(a: ArrayLike, axis: Axis = None,
                           dtype: DTypeLike = None, out: None = None) -> Array:
    return _cumulative_reduction(a, _ensure_optional_axes(axis), dtype, out)

  @partial(api.jit, static_argnames=('axis', 'dtype'))
  def _cumulative_reduction(a: ArrayLike, axis: Axis = None,
                            dtype: DTypeLike = None, out: None = None) -> Array:
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

    if not dtype and dtypes.dtype(a) == np.bool_:
      dtype = dtypes.canonicalize_dtype(dtypes.int_)
    if dtype:
      a = lax.convert_element_type(a, dtype)

    return reduction(a, axis)

  return cumulative_reduction
