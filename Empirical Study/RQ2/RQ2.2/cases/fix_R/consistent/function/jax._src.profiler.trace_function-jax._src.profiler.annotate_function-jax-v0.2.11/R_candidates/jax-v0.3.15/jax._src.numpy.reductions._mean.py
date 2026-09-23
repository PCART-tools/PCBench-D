@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'), inline=True)
def _mean(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
         out=None, keepdims=False, *, where=None):
  _check_arraylike("mean", a)
  lax_internal._check_user_dtype_supported(dtype, "mean")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.mean is not supported.")

  if where is None:
    if axis is None:
      normalizer = core.dimension_as_value(np.size(a))
    else:
      normalizer = core.dimension_as_value(_axis_size(a, axis))
  else:
    normalizer = sum(_broadcast_to(where, np.shape(a)), axis, dtype=dtype, keepdims=keepdims)

  if dtype is None:
    dtype = dtypes._to_inexact_dtype(dtypes.dtype(a))
  dtype = dtypes.canonicalize_dtype(dtype)

  return lax.div(
      sum(a, axis, dtype=dtype, keepdims=keepdims, where=where),
      lax.convert_element_type(normalizer, dtype))
