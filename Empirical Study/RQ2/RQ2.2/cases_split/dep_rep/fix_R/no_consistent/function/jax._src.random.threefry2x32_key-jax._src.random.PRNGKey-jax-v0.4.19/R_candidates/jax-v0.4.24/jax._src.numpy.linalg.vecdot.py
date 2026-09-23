@implements(getattr(np.linalg, "vecdot", None))
def vecdot(x1: ArrayLike, x2: ArrayLike, /, *, axis: int = -1) -> Array:
  return jnp.vecdot(x1, x2, axis=axis)
