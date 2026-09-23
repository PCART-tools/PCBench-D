@implements(getattr(np.linalg, "diagonal", None))
def diagonal(x: ArrayLike, /, *, offset: int = 0) -> Array:
  check_arraylike('jnp.linalg.diagonal', x)
  return jnp.diagonal(x, offset=offset, axis1=-2, axis2=-1)
