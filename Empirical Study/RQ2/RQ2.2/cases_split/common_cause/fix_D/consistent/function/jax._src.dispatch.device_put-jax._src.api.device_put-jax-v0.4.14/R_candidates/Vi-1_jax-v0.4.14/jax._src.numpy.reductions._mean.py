@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'), inline=True)
def _mean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None,
          out: None = None, keepdims: bool = False, *,
          where: Optional[ArrayLike] = None) -> Array:
  check_arraylike("mean", a)
  if dtype is None:
    dtype = dtypes.to_inexact_dtype(dtypes.dtype(a))
  else:
    dtypes.check_user_dtype_supported(dtype, "mean")
  dtype = dtypes.canonicalize_dtype(dtype)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.mean is not supported.")

  if where is None:
    if axis is None:
      normalizer = core.dimension_as_value(np.size(a))
    else:
      normalizer = core.dimension_as_value(_axis_size(a, axis))
  else:
    normalizer = sum(_broadcast_to(where, np.shape(a)), axis, dtype=dtype, keepdims=keepdims)

  return lax.div(
      sum(a, axis, dtype=dtype, keepdims=keepdims, where=where),
      lax.convert_element_type(normalizer, dtype))
