@implements(getattr(np.linalg, "vector_norm", None))
def vector_norm(x: ArrayLike, /, *, axis: int | None = None, keepdims: bool = False,
                ord: int | str = 2) -> Array:
  """Computes the vector norm of a vector (or batch of vectors) x."""
  check_arraylike('jnp.linalg.vector_norm', x)
  if axis is None:
    result = norm(jnp.ravel(x), ord=ord)
    if keepdims:
      result = lax.expand_dims(result, range(jnp.ndim(x)))
    return result
  return norm(x, axis=axis, keepdims=keepdims, ord=ord)
