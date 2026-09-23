@util.implements(np.empty_like, lax_description="""\
Because XLA cannot create uninitialized arrays, the JAX version will
return an array initialized with zeros.""")
def empty_like(prototype: ArrayLike | DuckTypedArray,
               dtype: DTypeLike | None = None,
               shape: Any = None, *,
               device: xc.Device | Sharding | None = None) -> Array:
  if not (hasattr(prototype, 'dtype') and hasattr(prototype, 'shape')):  # support duck typing
    util.check_arraylike("empty_like", prototype)
  dtypes.check_user_dtype_supported(dtype, "empty_like")
  return zeros_like(prototype, dtype=dtype, shape=shape, device=device)
