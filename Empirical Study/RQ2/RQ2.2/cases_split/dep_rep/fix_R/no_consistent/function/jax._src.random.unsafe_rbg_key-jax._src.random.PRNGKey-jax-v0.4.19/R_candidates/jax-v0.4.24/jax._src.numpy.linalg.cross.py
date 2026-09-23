@implements(getattr(np.linalg, "cross", None))
def cross(x1: ArrayLike, x2: ArrayLike, /, *, axis=-1):
  check_arraylike("jnp.linalg.outer", x1, x2)
  x1, x2 = jnp.asarray(x1), jnp.asarray(x2)
  if x1.shape[axis] != 3 or x2.shape[axis] != 3:
    raise ValueError(
        "Both input arrays must be (arrays of) 3-dimensional vectors, "
        f"but they have {x1.shape[axis]=} and {x2.shape[axis]=}"
    )
  return jnp.cross(x1, x2, axis=axis)
