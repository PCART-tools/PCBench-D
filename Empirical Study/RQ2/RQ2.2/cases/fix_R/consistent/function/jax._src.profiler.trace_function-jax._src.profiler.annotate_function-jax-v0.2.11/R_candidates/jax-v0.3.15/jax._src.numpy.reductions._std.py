@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def _std(a, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype=None,
        out=None, ddof=0, keepdims=False, *, where=None):
  _check_arraylike("std", a)
  lax_internal._check_user_dtype_supported(dtype, "std")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.std is not supported.")
  return lax.sqrt(var(a, axis=axis, dtype=dtype, ddof=ddof, keepdims=keepdims, where=where))
