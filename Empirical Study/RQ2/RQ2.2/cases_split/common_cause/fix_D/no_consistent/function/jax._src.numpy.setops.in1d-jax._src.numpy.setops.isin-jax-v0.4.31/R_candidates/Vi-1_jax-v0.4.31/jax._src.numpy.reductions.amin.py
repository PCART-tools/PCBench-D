def amin(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  """Alias of :func:`jax.numpy.min`."""
  return min(a, axis=axis, out=out, keepdims=keepdims,
             initial=initial, where=where)
