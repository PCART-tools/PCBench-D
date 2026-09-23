@_wraps(np.nanmean, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanmean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None, out: None = None,
            keepdims: bool = False, where: Optional[ArrayLike] = None) -> Array:
  _check_arraylike("nanmean", a)
  dtypes.check_user_dtype_supported(dtype, "nanmean")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanmean is not supported.")
  if dtypes.issubdtype(dtypes.dtype(a), np.bool_) or dtypes.issubdtype(dtypes.dtype(a), np.integer):
    return mean(a, axis, dtype, out, keepdims, where=where)
  if dtype is None:
    dtype = dtypes.dtype(a)
  nan_mask = lax_internal.bitwise_not(lax_internal._isnan(a))
  normalizer = sum(nan_mask, axis=axis, dtype=np.int32, keepdims=keepdims, where=where)
  normalizer = lax.convert_element_type(normalizer, dtype)
  td = lax.div(nansum(a, axis, dtype=dtype, keepdims=keepdims, where=where), normalizer)
  return td
