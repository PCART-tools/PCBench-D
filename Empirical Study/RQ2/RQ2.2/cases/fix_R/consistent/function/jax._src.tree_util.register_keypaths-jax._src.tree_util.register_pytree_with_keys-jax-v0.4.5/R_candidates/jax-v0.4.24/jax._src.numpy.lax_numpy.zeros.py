@util.implements(np.zeros)
def zeros(shape: Any, dtype: DTypeLike | None = None, *,
          device: xc.Device | Sharding | None = None) -> Array:
  if isinstance(shape, types.GeneratorType):
    raise TypeError("expected sequence object with len >= 0 or a single integer")
  if (m := _check_forgot_shape_tuple("zeros", shape, dtype)): raise TypeError(m)
  dtypes.check_user_dtype_supported(dtype, "zeros")
  shape = canonicalize_shape(shape)
  return lax.full(shape, 0, _jnp_dtype(dtype), sharding=_normalize_to_sharding(device))
