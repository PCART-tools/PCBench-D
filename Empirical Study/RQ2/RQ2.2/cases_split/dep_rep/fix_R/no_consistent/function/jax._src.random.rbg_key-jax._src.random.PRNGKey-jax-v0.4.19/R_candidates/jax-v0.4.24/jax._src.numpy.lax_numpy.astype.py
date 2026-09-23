@util.implements(getattr(np, "astype", None), lax_description="""
This is implemented via :func:`jax.lax.convert_element_type`, which may
have slightly different behavior than :func:`numpy.astype` in some cases.
In particular, the details of float-to-int and int-to-float casts are
implementation dependent.
""")
def astype(x: ArrayLike, dtype: DTypeLike | None, /, *, copy: bool = True) -> Array:
  del copy  # unused in JAX
  if dtype is None:
    dtype = dtypes.canonicalize_dtype(float_)
  dtypes.check_user_dtype_supported(dtype, "astype")
  return lax.convert_element_type(x, dtype)
