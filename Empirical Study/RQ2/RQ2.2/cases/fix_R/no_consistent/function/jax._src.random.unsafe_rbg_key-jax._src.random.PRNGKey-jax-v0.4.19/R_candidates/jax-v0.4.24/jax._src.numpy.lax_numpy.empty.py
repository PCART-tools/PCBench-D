@util.implements(np.empty, lax_description="""\
Because XLA cannot create uninitialized arrays, the JAX version will
return an array initialized with zeros.""")
def empty(shape: Any, dtype: DTypeLike | None = None, *,
          device: xc.Device | Sharding | None = None) -> Array:
  if (m := _check_forgot_shape_tuple("empty", shape, dtype)): raise TypeError(m)
  dtypes.check_user_dtype_supported(dtype, "empty")
  return zeros(shape, dtype, device=device)
