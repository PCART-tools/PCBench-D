@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def _std(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None,
         out: None = None, ddof: int = 0, keepdims: bool = False, *,
         where: Optional[ArrayLike] = None) -> Array:
  check_arraylike("std", a)
  dtypes.check_user_dtype_supported(dtype, "std")
  if dtype is not None and not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"dtype argument to jnp.std must be inexact; got {dtype}")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.std is not supported.")
  return lax.sqrt(var(a, axis=axis, dtype=dtype, ddof=ddof, keepdims=keepdims, where=where))
