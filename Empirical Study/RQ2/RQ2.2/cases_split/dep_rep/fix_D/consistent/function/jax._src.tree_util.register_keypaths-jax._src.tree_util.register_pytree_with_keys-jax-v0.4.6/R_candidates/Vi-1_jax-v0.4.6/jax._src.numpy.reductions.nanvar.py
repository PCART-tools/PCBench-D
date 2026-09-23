@_wraps(np.nanvar, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanvar(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None, out: None = None,
           ddof: int = 0, keepdims: bool = False,
           where: Optional[ArrayLike] = None) -> Array:
  _check_arraylike("nanvar", a)
  dtypes.check_user_dtype_supported(dtype, "nanvar")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanvar is not supported.")

  computation_dtype, dtype = _var_promote_types(dtypes.dtype(a), dtype)
  a = _asarray(a).astype(computation_dtype)
  a_mean = nanmean(a, axis, dtype=computation_dtype, keepdims=True, where=where)

  centered = _where(lax_internal._isnan(a), 0, lax.sub(a, a_mean))  # double-where trick for gradients.
  if dtypes.issubdtype(centered.dtype, np.complexfloating):
    centered = lax.real(lax.mul(centered, lax.conj(centered)))
  else:
    centered = lax.square(centered)

  normalizer = sum(lax_internal.bitwise_not(lax_internal._isnan(a)),
                   axis=axis, keepdims=keepdims, where=where)
  normalizer = normalizer - ddof
  normalizer_mask = lax.le(normalizer, lax_internal._zero(normalizer))
  result = sum(centered, axis, keepdims=keepdims, where=where)
  result = _where(normalizer_mask, np.nan, result)
  divisor = _where(normalizer_mask, 1, normalizer)
  result = lax.div(result, lax.convert_element_type(divisor, result.dtype))
  return lax.convert_element_type(result, dtype)
