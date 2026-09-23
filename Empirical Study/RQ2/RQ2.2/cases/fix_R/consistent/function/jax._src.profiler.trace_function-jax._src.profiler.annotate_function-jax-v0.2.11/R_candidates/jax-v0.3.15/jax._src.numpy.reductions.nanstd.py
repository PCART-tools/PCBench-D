@_wraps(np.nanstd, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanstd(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
           out=None, ddof=0, keepdims=False, where=None):
  _check_arraylike("nanstd", a)
  lax_internal._check_user_dtype_supported(dtype, "nanstd")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanstd is not supported.")
  return lax.sqrt(nanvar(a, axis=axis, dtype=dtype, ddof=ddof, keepdims=keepdims, where=where))
