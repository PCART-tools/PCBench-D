@implements(getattr(np.linalg, "outer", None))
def outer(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  check_arraylike("jnp.linalg.outer", x1, x2)
  x1, x2 = jnp.asarray(x1), jnp.asarray(x2)
  if x1.ndim != 1 or x2.ndim != 1:
    raise ValueError(f"Input arrays must be one-dimensional, but they are {x1.ndim=} {x2.ndim=}")
  return x1[:, None] * x2[None, :]
