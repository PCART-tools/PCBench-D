@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def _var(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, correction: int | float = 0, keepdims: bool = False, *,
         where: ArrayLike | None = None) -> Array:
  check_arraylike("var", a)
  dtypes.check_user_dtype_supported(dtype, "var")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.var is not supported.")

  computation_dtype, dtype = _var_promote_types(dtypes.dtype(a), dtype)
  a = lax_internal.asarray(a).astype(computation_dtype)
  a_mean = mean(a, axis, dtype=computation_dtype, keepdims=True, where=where)
  centered = lax.sub(a, a_mean)
  if dtypes.issubdtype(computation_dtype, np.complexfloating):
    centered = lax.real(lax.mul(centered, lax.conj(centered)))
    computation_dtype = centered.dtype  # avoid casting to complex below.
  else:
    centered = lax.square(centered)

  if where is None:
    if axis is None:
      normalizer = core.dimension_as_value(np.size(a))
    else:
      normalizer = core.dimension_as_value(_axis_size(a, axis))
    normalizer = lax.convert_element_type(normalizer, computation_dtype)
  else:
    normalizer = sum(_broadcast_to(where, np.shape(a)), axis,
                     dtype=computation_dtype, keepdims=keepdims)
  normalizer = lax.sub(normalizer, lax.convert_element_type(correction, computation_dtype))
  result = sum(centered, axis, dtype=computation_dtype, keepdims=keepdims, where=where)
  result = lax.div(result, normalizer).astype(dtype)
  with jax.debug_nans(False):
    result = _where(normalizer > 0, result, np.nan)
  return result
