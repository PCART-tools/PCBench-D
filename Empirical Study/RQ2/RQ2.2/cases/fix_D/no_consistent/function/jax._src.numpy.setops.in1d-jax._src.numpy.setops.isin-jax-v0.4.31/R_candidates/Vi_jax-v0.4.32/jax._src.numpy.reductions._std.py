@partial(api.jit, static_argnames=('axis', 'dtype', 'keepdims'))
def _std(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, correction: int | float = 0, keepdims: bool = False, *,
         where: ArrayLike | None = None) -> Array:
  check_arraylike("std", a)
  dtypes.check_user_dtype_supported(dtype, "std")
  if dtype is not None and not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"dtype argument to jnp.std must be inexact; got {dtype}")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.std is not supported.")
  return lax.sqrt(var(a, axis=axis, dtype=dtype, correction=correction, keepdims=keepdims, where=where))
