@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def _var(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None,
         out: None = None, ddof: int = 0, keepdims: bool = False, *,
         where: Optional[ArrayLike] = None) -> Array:
  _check_arraylike("var", a)
  dtypes.check_user_dtype_supported(dtype, "var")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.var is not supported.")

  computation_dtype, dtype = _var_promote_types(dtypes.dtype(a), dtype)
  a = _asarray(a).astype(computation_dtype)
  a_mean = mean(a, axis, dtype=computation_dtype, keepdims=True, where=where)
  centered = lax.sub(a, a_mean)
  if dtypes.issubdtype(centered.dtype, np.complexfloating):
    centered = lax.real(lax.mul(centered, lax.conj(centered)))
  else:
    centered = lax.square(centered)

  if where is None:
    if axis is None:
      normalizer = core.dimension_as_value(np.size(a))
    else:
      normalizer = core.dimension_as_value(_axis_size(a, axis))
  else:
    normalizer = sum(_broadcast_to(where, np.shape(a)), axis, dtype=dtype, keepdims=keepdims)
  normalizer = normalizer - ddof

  result = sum(centered, axis, keepdims=keepdims, where=where)
  result = lax.div(result, lax.convert_element_type(normalizer, result.dtype))
  return lax.convert_element_type(result, dtype)
