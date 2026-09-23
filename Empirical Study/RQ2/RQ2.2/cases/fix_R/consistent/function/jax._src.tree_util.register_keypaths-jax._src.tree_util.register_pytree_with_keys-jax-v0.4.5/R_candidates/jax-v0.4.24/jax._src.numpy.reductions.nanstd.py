@implements(np.nanstd, skip_params=['out'])
@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def nanstd(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
           ddof: int = 0, keepdims: bool = False,
           where: ArrayLike | None = None) -> Array:
  check_arraylike("nanstd", a)
  dtypes.check_user_dtype_supported(dtype, "nanstd")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanstd is not supported.")
  return lax.sqrt(nanvar(a, axis=axis, dtype=dtype, ddof=ddof, keepdims=keepdims, where=where))
