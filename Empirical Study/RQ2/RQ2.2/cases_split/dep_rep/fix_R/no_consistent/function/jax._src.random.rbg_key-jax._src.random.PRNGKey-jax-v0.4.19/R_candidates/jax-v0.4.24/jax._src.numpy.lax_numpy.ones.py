@util.implements(np.ones)
def ones(shape: Any, dtype: DTypeLike | None = None, *,
         device: xc.Device | Sharding | None = None) -> Array:
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  if (m := _check_forgot_shape_tuple("ones", shape, dtype)): raise TypeError(m)
  shape = canonicalize_shape(shape)
  dtypes.check_user_dtype_supported(dtype, "ones")
  return lax.full(shape, 1, _jnp_dtype(dtype), sharding=_normalize_to_sharding(device))
