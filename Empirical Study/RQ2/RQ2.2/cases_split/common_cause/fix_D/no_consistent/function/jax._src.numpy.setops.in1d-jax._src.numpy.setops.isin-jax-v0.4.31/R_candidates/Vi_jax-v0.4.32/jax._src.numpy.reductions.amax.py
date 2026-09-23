def amax(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  """Alias of :func:`jax.numpy.max`."""
  return max(a, axis=axis, out=out, keepdims=keepdims,
             initial=initial, where=where)
