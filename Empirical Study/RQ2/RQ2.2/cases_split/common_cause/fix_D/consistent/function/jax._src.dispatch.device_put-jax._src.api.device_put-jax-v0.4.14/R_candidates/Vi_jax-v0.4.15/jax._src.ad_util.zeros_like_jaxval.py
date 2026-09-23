def zeros_like_jaxval(val: ArrayLike) -> Array:
  return zeros_like_p.bind(val)
