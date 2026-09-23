@implements(getattr(np.linalg, "matmul", None))
def matmul(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  check_arraylike('jnp.linalg.matmul', x1, x2)
  return jnp.matmul(x1, x2)
